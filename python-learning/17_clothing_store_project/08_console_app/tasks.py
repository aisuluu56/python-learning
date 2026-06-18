"""
Этап 08. Итоговое консольное приложение
"""

from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорты
domain_models = import_module("01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product
SizeStock = domain_models.SizeStock
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

user_module = import_module("07_users_discounts.tasks")
DeliveryAddress = user_module.DeliveryAddress
Promocode = user_module.Promocode
AddressRepository = user_module.AddressRepository
PromocodeRepository = user_module.PromocodeRepository
DiscountService = user_module.DiscountService
ExtendedOrderService = user_module.ExtendedOrderService

db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


class StoreApp:
    def __init__(self, conn):
        self.conn = conn
        
        # Создаем репозитории
        self.cat_repo = CategoryRepository(conn)
        self.prod_repo = ProductRepository(conn)
        self.stock_repo = StockRepository(conn)
        self.cust_repo = CustomerRepository(conn)
        self.addr_repo = AddressRepository(conn)
        self.promo_repo = PromocodeRepository(conn)
        self.order_repo = OrderRepository(conn)
        
        # Создаем сервисы
        self.catalog = CatalogService(self.prod_repo, self.cat_repo, self.stock_repo)
        self.cart_service = CartService(self.catalog, self.stock_repo)
        self.discount = DiscountService(self.promo_repo)
        self.order_service = ExtendedOrderService(
            self.stock_repo, self.cust_repo, self.order_repo, conn, self.discount
        )
        
        # Текущий пользователь
        self.customer = None
    
    def create_test_data(self):
        """Создает тестовые данные если их нет"""
        print("Создаю тестовые данные...")
        
        # Категории
        cat1 = Category(None, "Футболки", "Хлопковые")
        cat2 = Category(None, "Джинсы", "Джинсовая ткань")
        
        c1 = self.cat_repo.add(cat1)
        c2 = self.cat_repo.add(cat2)
        
        cat1 = self.cat_repo.get_by_id(c1)
        cat2 = self.cat_repo.get_by_id(c2)
        
        # Товары
        prod1 = Product(None, "Белая футболка", cat1, 1999, "Белый", "", True)
        prod2 = Product(None, "Синяя футболка", cat1, 2299, "Синий", "", True)
        prod3 = Product(None, "Классические джинсы", cat2, 3999, "Синий", "", True)
        
        p1 = self.prod_repo.add(prod1)
        p2 = self.prod_repo.add(prod2)
        p3 = self.prod_repo.add(prod3)
        
        prod1 = self.prod_repo.get_by_id(p1, self.cat_repo)
        prod2 = self.prod_repo.get_by_id(p2, self.cat_repo)
        prod3 = self.prod_repo.get_by_id(p3, self.cat_repo)
        
        # Остатки
        p = Product(p1, "", None, 0, "")
        self.stock_repo.add(SizeStock(p, "M", 10))
        self.stock_repo.add(SizeStock(p, "L", 5))
        
        p = Product(p2, "", None, 0, "")
        self.stock_repo.add(SizeStock(p, "S", 8))
        self.stock_repo.add(SizeStock(p, "M", 12))
        
        p = Product(p3, "", None, 0, "")
        self.stock_repo.add(SizeStock(p, "32", 7))
        self.stock_repo.add(SizeStock(p, "34", 5))
        
        # Покупатель
        cust = Customer(None, "Иван Петров", "+79991234567", "ivan@mail.ru")
        cid = self.cust_repo.add(cust)
        cust = self.cust_repo.get_by_id(cid)
        
        # Адрес
        addr = DeliveryAddress(cid, "ул. Ленина 15", "Москва", "101000", True)
        self.addr_repo.add(addr)
        
        # Промокод
        promo = Promocode("DISCOUNT10", 10)
        self.promo_repo.add(promo)
        
        self.customer = cust
        print("Тестовые данные созданы!\n")
    
    def show_menu(self):
        print("\n" + "=" * 40)
        print("МАГАЗИН ОДЕЖДЫ")
        print("=" * 40)
        if self.customer:
            print(f"Покупатель: {self.customer.full_name}")
        print("-" * 40)
        print("1. Каталог")
        print("2. Поиск")
        print("3. Фильтр")
        print("4. Корзина")
        print("5. Добавить в корзину")
        print("6. Удалить из корзины")
        print("7. Применить промокод")
        print("8. Оформить заказ")
        print("9. История заказов")
        print("0. Выход")
        print("=" * 40)
    
    def show_catalog(self):
        print("\nКАТАЛОГ:")
        products = self.catalog.get_active_products()
        for p in products:
            print(f"{p.product_id}. {p.name} - {p.price} руб. ({p.color})")
    
    def search(self):
        query = input("Введите название: ")
        products = self.catalog.search_by_name(query)
        if products:
            for p in products:
                print(f"{p.product_id}. {p.name} - {p.price} руб.")
        else:
            print("Ничего не найдено")
    
    def filter_products(self):
        color = input("Цвет (пусто - все): ")
        min_price = input("Мин цена (пусто - 0): ")
        max_price = input("Макс цена (пусто - все): ")
        
        min_p = int(min_price) if min_price else 0
        max_p = int(max_price) if max_price else 999999
        
        products = self.catalog.filter_by_price(min_p, max_p)
        if color:
            products = [p for p in products if p.color.lower() == color.lower()]
        
        if products:
            for p in products:
                print(f"{p.product_id}. {p.name} - {p.price} руб.")
        else:
            print("Товаров нет")
    
    def show_cart(self):
        print(self.cart_service.get_cart_summary())
    
    def add_to_cart(self):
        try:
            pid = int(input("ID товара: "))
            size = input("Размер: ").upper()
            qty = int(input("Количество: "))
            
            product = self.catalog.get_product_by_id(pid)
            if not product:
                print("Товар не найден")
                return
            
            self.cart_service.add_to_cart(product, size, qty)
            print("Товар добавлен!")
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    def remove_from_cart(self):
        try:
            pid = int(input("ID товара: "))
            size = input("Размер: ").upper()
            self.cart_service.remove_from_cart(pid, size)
            print("Товар удален!")
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    def apply_promo(self):
        code = input("Введите промокод: ").upper()
        try:
            total = self.cart_service.get_total()
            new_total = self.discount.apply_promocode(total, code)
            print(f"Сумма со скидкой: {new_total} руб.")
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    def checkout(self):
        if self.cart_service.get_cart().is_empty():
            print("Корзина пуста!")
            return
        
        print("Ваш заказ:")
        print(self.cart_service.get_cart_summary())
        
        confirm = input("Оформить заказ? (y/n): ")
        if confirm.lower() != 'y':
            return
        
        try:
            order_id = self.order_service.create_order(
                self.cart_service.get_cart(), 
                self.customer.customer_id
            )
            print(f"Заказ #{order_id} оформлен!")
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    def order_history(self):
        orders = self.order_repo.get_by_customer(self.customer.customer_id, self.cust_repo)
        if not orders:
            print("Заказов нет")
            return
        
        for o in orders:
            print(f"Заказ #{o.order_id}: {o.status}, {o.total_amount} руб.")
    
    def run(self):
        self.create_test_data()
        
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.show_catalog()
            elif choice == "2":
                self.search()
            elif choice == "3":
                self.filter_products()
            elif choice == "4":
                self.show_cart()
            elif choice == "5":
                self.add_to_cart()
            elif choice == "6":
                self.remove_from_cart()
            elif choice == "7":
                self.apply_promo()
            elif choice == "8":
                self.checkout()
            elif choice == "9":
                self.order_history()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор")


if __name__ == "__main__":
    conn = get_connection()
    app = StoreApp(conn)
    app.run()
    conn.close()