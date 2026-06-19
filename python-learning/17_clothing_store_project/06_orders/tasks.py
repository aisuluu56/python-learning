"""
Этап 06. Заказы
"""

from importlib import import_module
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Задание 1
# Импортируем все необходимое

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

db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


# Задание 2
# Модель позиции заказа

class OrderItem:
    def __init__(self, product_id, product_name, size, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.size = size
        self.price = price
        self.quantity = quantity

    def get_total(self):
        return self.price * self.quantity


# Задание 3
# Модель заказа

class Order:
    def __init__(self, customer, items, total_amount):
        self.customer = customer
        self.items = items
        self.total_amount = total_amount
        self.status = "new"
        self.order_date = datetime.now()

    def cancel(self):
        if self.status in ["delivered", "cancelled"]:
            raise ValueError("Нельзя отменить этот заказ")
        self.status = "cancelled"


# Задание 4
# Репозиторий заказов

class OrderRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, order):
        with self.conn.cursor() as cursor:
            # Сохраняем заказ
            sql = """
                INSERT INTO orders (customer_id, total_amount, status, order_date)
                VALUES (%s, %s, %s, %s) RETURNING id
            """
            cursor.execute(sql, (order.customer.customer_id, order.total_amount, 
                               order.status, order.order_date))
            order_id = cursor.fetchone()[0]
            
            # Сохраняем позиции
            for item in order.items:
                sql = """
                    INSERT INTO order_items (order_id, product_id, product_name, size, price, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (order_id, item.product_id, item.product_name,
                                   item.size, item.price, item.quantity))
            
            self.conn.commit()
            return order_id


# Задание 5
# Сервис заказов

class OrderService:
    def __init__(self, stock_repo, customer_repo, order_repo, conn):
        self.stock_repo = stock_repo
        self.customer_repo = customer_repo
        self.order_repo = order_repo
        self.conn = conn

    def create_order(self, cart, customer_id):
        # Проверяем покупателя
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise ValueError("Покупатель не найден")
        
        # Проверяем корзину
        if cart.is_empty():
            raise ValueError("Корзина пуста")
        
        # Проверяем остатки и создаем позиции
        items = []
        total = 0
        
        for cart_item in cart.get_items():
            product = cart_item.product
            available = self.stock_repo.get_quantity(product.product_id, cart_item.size)
            
            if available < cart_item.quantity:
                raise ValueError(f"Недостаточно {product.name} размера {cart_item.size}")
            
            # Создаем позицию заказа
            item = OrderItem(
                product.product_id,
                product.name,
                cart_item.size,
                cart_item.price,
                cart_item.quantity
            )
            items.append(item)
            total += item.get_total()
        
        # Создаем заказ
        order = Order(customer, items, total)
        
        # Уменьшаем остатки
        for cart_item in cart.get_items():
            current = self.stock_repo.get_quantity(cart_item.product.product_id, cart_item.size)
            new_qty = current - cart_item.quantity
            self.stock_repo.update_quantity(cart_item.product.product_id, cart_item.size, new_qty)
        
        # Сохраняем заказ
        order_id = self.order_repo.save(order)
        
        # Очищаем корзину
        cart.clear()
        
        return order_id


# Задание 6
# Проверка работы

if __name__ == "__main__":
    conn = get_connection()
    
    category_repo = CategoryRepository(conn)
    product_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    customer_repo = CustomerRepository(conn)
    order_repo = OrderRepository(conn)
    
    catalog = CatalogService(product_repo, category_repo, stock_repo)
    cart_service = CartService(catalog, stock_repo)
    order_service = OrderService(stock_repo, customer_repo, order_repo, conn)
    
    # Создаем тестовые данные
    # Исправление: создаем категорию без ID (None), репозиторий сам присвоит ID
    category = Category(None, "Футболки", "Хлопковые")
    cat_id = category_repo.add(category)
    # Получаем категорию с ID из БД
    category = category_repo.get_by_id(cat_id)
    
    # Исправление: создаем продукт с None ID
    product = Product(None, "Белая футболка", category, 1999, "Белый", "", True)
    prod_id = product_repo.add(product)
    # Получаем продукт с ID из БД
    product = product_repo.get_by_id(prod_id, category_repo)
    
    # Исправление: создаем объект Product для остатков
    # Используем существующий продукт с ID
    stock_repo.add(SizeStock(product, "M", 10))
    
    # Создаем покупателя
    customer = Customer(None, "Иван Петров", "+7(999)123-45-67", "ivan@mail.ru")
    cust_id = customer_repo.add(customer)
    customer = customer_repo.get_by_id(cust_id)
    
    print("1. ДОБАВЛЯЕМ ТОВАР В КОРЗИНУ")
    cart_service.add_to_cart(prod_id, "M", 3)
    print(cart_service.get_cart_summary())
    
    print("\n2. ОФОРМЛЯЕМ ЗАКАЗ")
    order_id = order_service.create_order(cart_service.get_cart(), cust_id)
    print(f"Заказ #{order_id} создан успешно!")
    
    print("\n3. ПРОВЕРЯЕМ ОСТАТКИ")
    остаток = stock_repo.get_quantity(prod_id, "M")
    print(f"Остаток M: {остаток} шт.")
    
    print("\n4. КОРЗИНА ПОСЛЕ ЗАКАЗА")
    print(cart_service.get_cart_summary())
    
    print("\n5. ПЫТАЕМСЯ СОЗДАТЬ ЗАКАЗ С ПУСТОЙ КОРЗИНОЙ")
    try:
        order_service.create_order(cart_service.get_cart(), cust_id)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    conn.close()