"""
Этап 07. Пользователи и скидки
"""

from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорты
domain_models = import_module("01_domain_models.tasks")
Product = domain_models.Product
SizeStock = domain_models.SizeStock
Category = domain_models.Category
Customer = domain_models.Customer

repos_module = import_module("03_repositories.tasks")
CategoryRepository = repos_module.CategoryRepository
ProductRepository = repos_module.ProductRepository
StockRepository = repos_module.StockRepository
CustomerRepository = repos_module.CustomerRepository

cart_module = import_module("05_cart.tasks")
Cart = cart_module.Cart
CartItem = cart_module.CartItem
CartService = cart_module.CartService

catalog_module = import_module("04_catalog_service.tasks")
CatalogService = catalog_module.CatalogService

order_module = import_module("06_orders.tasks")
Order = order_module.Order
OrderItem = order_module.OrderItem
OrderRepository = order_module.OrderRepository
OrderService = order_module.OrderService

db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


# Модель адреса
class DeliveryAddress:
    def __init__(self, customer_id, address, city, postal_code="", is_default=False):
        self.customer_id = customer_id
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.is_default = is_default


# Репозиторий адресов
class AddressRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, address):
        sql = """
            INSERT INTO delivery_addresses (customer_id, address, city, postal_code, is_default)
            VALUES (%s, %s, %s, %s, %s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (address.customer_id, address.address, address.city,
                               address.postal_code, address.is_default))
            self.conn.commit()

    def get_by_customer(self, customer_id):
        sql = "SELECT address, city, postal_code FROM delivery_addresses WHERE customer_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (customer_id,))
            rows = cursor.fetchall()
            addresses = []
            for row in rows:
                addresses.append(DeliveryAddress(customer_id, row[0], row[1], row[2]))
            return addresses


# Модель промокода
class Promocode:
    def __init__(self, code, discount_percent, min_order=0):
        self.code = code.upper()
        self.discount_percent = discount_percent
        self.min_order = min_order

    def apply(self, total):
        if total < self.min_order:
            raise ValueError(f"Минимальная сумма {self.min_order} руб.")
        
        discount = total * self.discount_percent // 100
        return total - discount


# Репозиторий промокодов
class PromocodeRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, promocode):
        sql = "INSERT INTO promocodes (code, discount_percent, min_order_amount) VALUES (%s, %s, %s)"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (promocode.code, promocode.discount_percent, promocode.min_order))
            self.conn.commit()

    def get_by_code(self, code):
        sql = "SELECT code, discount_percent, min_order_amount FROM promocodes WHERE code = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (code.upper(),))
            row = cursor.fetchone()
            if row:
                return Promocode(row[0], row[1], row[2])
            return None


# Сервис скидок
class DiscountService:
    def __init__(self, promo_repo):
        self.promo_repo = promo_repo

    def apply_promocode(self, total, code):
        promo = self.promo_repo.get_by_code(code)
        if not promo:
            raise ValueError("Промокод не найден")
        
        new_total = promo.apply(total)
        return new_total


# Расширенный сервис заказов со скидкой
class ExtendedOrderService(OrderService):
    def __init__(self, stock_repo, customer_repo, order_repo, conn, discount_service=None):
        super().__init__(stock_repo, customer_repo, order_repo, conn)
        self.discount_service = discount_service

    def create_order(self, cart, customer_id, promo_code=None):
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise ValueError("Покупатель не найден")
        
        if cart.is_empty():
            raise ValueError("Корзина пуста")
        
        # Создаем позиции заказа
        items = []
        total = 0
        
        for cart_item in cart.get_items():
            product = cart_item.product
            available = self.stock_repo.get_quantity(product.product_id, cart_item.size)
            
            if available < cart_item.quantity:
                raise ValueError(f"Недостаточно {product.name}")
            
            item = OrderItem(
                product.product_id,
                product.name,
                cart_item.size,
                cart_item.price,
                cart_item.quantity
            )
            items.append(item)
            total += item.get_total()
        
        # Применяем скидку
        if self.discount_service and promo_code:
            total = self.discount_service.apply_promocode(total, promo_code)
        
        # Создаем заказ
        order = Order(customer, items, total)
        
        # Уменьшаем остатки
        for cart_item in cart.get_items():
            current = self.stock_repo.get_quantity(cart_item.product.product_id, cart_item.size)
            new_qty = current - cart_item.quantity
            self.stock_repo.update_quantity(cart_item.product.product_id, cart_item.size, new_qty)
        
        order_id = self.order_repo.save(order)
        cart.clear()
        
        return order_id


# Проверка
if __name__ == "__main__":
    conn = get_connection()
    
    category_repo = CategoryRepository(conn)
    product_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    customer_repo = CustomerRepository(conn)
    address_repo = AddressRepository(conn)
    promo_repo = PromocodeRepository(conn)
    order_repo = OrderRepository(conn)
    
    catalog = CatalogService(product_repo, category_repo, stock_repo)
    cart_service = CartService(catalog, stock_repo)
    discount_service = DiscountService(promo_repo)
    order_service = ExtendedOrderService(stock_repo, customer_repo, order_repo, conn, discount_service)
    
    # Создаем товар
    category = Category(None, "Футболки", "")
    cat_id = category_repo.add(category)
    category = category_repo.get_by_id(cat_id)
    
    product = Product(None, "Футболка", category, 1999, "Белый", "", True)
    prod_id = product_repo.add(product)
    product = product_repo.get_by_id(prod_id, category_repo)
    
    prod = Product(prod_id, "", None, 0, "")
    stock_repo.add(SizeStock(prod, "M", 10))
    
    # Создаем покупателя
    customer = Customer(None, "Иван", "+79991234567", "ivan@mail.ru")
    cust_id = customer_repo.add(customer)
    
    # Добавляем адрес
    address = DeliveryAddress(cust_id, "ул. Ленина 15", "Москва", "101000")
    address_repo.add(address)
    
    # Добавляем промокод
    promo = Promocode("DISCOUNT10", 10)
    promo_repo.add(promo)
    
    # Добавляем в корзину
    cart_service.add_to_cart(prod_id, "M", 2)
    print(cart_service.get_cart_summary())
    
    # Применяем промокод
    total = cart_service.get_total()
    print(f"\nСумма: {total} руб.")
    
    new_total = discount_service.apply_promocode(total, "DISCOUNT10")
    print(f"Со скидкой: {new_total} руб.")
    
    # Оформляем заказ
    order_id = order_service.create_order(cart_service.get_cart(), cust_id, "DISCOUNT10")
    print(f"\nЗаказ #{order_id} создан!")
    
    # Проверяем адреса
    print("\nАдреса покупателя:")
    for addr in address_repo.get_by_customer(cust_id):
        print(f"  {addr.address}, {addr.city}")
    
    conn.close()