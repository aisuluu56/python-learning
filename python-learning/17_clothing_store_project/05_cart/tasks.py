"""
Этап 05. Корзина
"""

from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Задание 1
# Импортируйте модели и сервис каталога

# TODO: подготовить товары для корзины

domain_models = import_module("01_domain_models.tasks")
Product = domain_models.Product
SizeStock = domain_models.SizeStock
Category = domain_models.Category

repos_module = import_module("03_repositories.tasks")
CategoryRepository = repos_module.CategoryRepository
ProductRepository = repos_module.ProductRepository
StockRepository = repos_module.StockRepository

catalog_module = import_module("04_catalog_service.tasks")
CatalogService = catalog_module.CatalogService

db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


# Задание 2
# Опишите позицию корзины

# TODO: добавить модель позиции корзины

class CartItem:
    def __init__(self, product, size, quantity):
        self.product = product
        self.size = size
        self.quantity = quantity
        self.price = product.price

    def get_total(self):
        return self.price * self.quantity


# Задание 3
# Опишите корзину

# TODO: добавить модель корзины

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, size, quantity):
        # Проверяем есть ли уже такой товар
        for item in self.items:
            if item.product.product_id == product.product_id and item.size == size:
                item.quantity += quantity
                return
        
        # Если нет - создаем новый
        self.items.append(CartItem(product, size, quantity))

    def remove_item(self, product_id, size):
        for i, item in enumerate(self.items):
            if item.product.product_id == product_id and item.size == size:
                self.items.pop(i)
                return

    def update_quantity(self, product_id, size, new_quantity):
        for item in self.items:
            if item.product.product_id == product_id and item.size == size:
                if new_quantity <= 0:
                    self.remove_item(product_id, size)
                else:
                    item.quantity = new_quantity
                return

    def get_total(self):
        total = 0
        for item in self.items:
            total += item.get_total()
        return total

    def clear(self):
        self.items = []

    def get_items(self):
        return self.items

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        if not self.items:
            return "Корзина пуста"
        
        result = []
        for item in self.items:
            result.append(f"{item.product.name} ({item.size}) x{item.quantity} = {item.get_total()} руб.")
        result.append(f"Итого: {self.get_total()} руб.")
        return "\n".join(result)


# Задание 4-6 уже сделаны в классе Cart


# Задание 7
# Создайте сервис корзины

# TODO: отделить бизнес-проверки корзины

class CartService:
    def __init__(self, catalog_service, stock_repo):
        self.catalog_service = catalog_service
        self.stock_repo = stock_repo
        self.cart = Cart()

    def add_to_cart(self, product_id, size, quantity):
        # Получаем товар
        product = self.catalog_service.get_product_by_id(product_id)
        if not product:
            raise ValueError("Товар не найден")
        
        if not product.is_active:
            raise ValueError("Товар неактивен")
        
        # Проверяем остаток
        available = self.stock_repo.get_quantity(product_id, size)
        if available < quantity:
            raise ValueError(f"Недостаточно товара. Доступно: {available}")
        
        # Добавляем в корзину
        self.cart.add_item(product, size, quantity)

    def update_quantity(self, product_id, size, new_quantity):
        if new_quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        
        if new_quantity == 0:
            self.cart.remove_item(product_id, size)
            return
        
        # Проверяем остаток
        available = self.stock_repo.get_quantity(product_id, size)
        if available < new_quantity:
            raise ValueError(f"Недостаточно товара. Доступно: {available}")
        
        self.cart.update_quantity(product_id, size, new_quantity)

    def remove_from_cart(self, product_id, size):
        self.cart.remove_item(product_id, size)

    def get_total(self):
        return self.cart.get_total()

    def clear_cart(self):
        self.cart.clear()

    def get_cart_summary(self):
        return str(self.cart)


# Задание 8
# Проверьте работу корзины

# TODO: добавить ручную проверку

if __name__ == "__main__":
    conn = get_connection()
    
    category_repo = CategoryRepository(conn)
    product_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    
    catalog = CatalogService(product_repo, category_repo, stock_repo)
    cart_service = CartService(catalog, stock_repo)
    
    # Создаем тестовые данные
    category = Category(None, "Футболки", "Хлопковые")
    cat_id = category_repo.add(category)
    category = category_repo.get_by_id(cat_id)
    
    product = Product(None, "Белая футболка", category, 1999, "Белый", "", True)
    prod_id = product_repo.add(product)
    product = product_repo.get_by_id(prod_id, category_repo)
    
    # Добавляем остатки
    prod = Product(prod_id, "", None, 0, "")
    stock_repo.add(SizeStock(prod, "M", 10))
    stock_repo.add(SizeStock(prod, "L", 5))
    
    print("1. ДОБАВЛЯЕМ ТОВАР")
    cart_service.add_to_cart(prod_id, "M", 2)
    print(cart_service.get_cart_summary())
    
    print("\n2. УВЕЛИЧИВАЕМ КОЛИЧЕСТВО")
    cart_service.update_quantity(prod_id, "M", 5)
    print(cart_service.get_cart_summary())
    
    print("\n3. УМЕНЬШАЕМ КОЛИЧЕСТВО")
    cart_service.update_quantity(prod_id, "M", 3)
    print(cart_service.get_cart_summary())
    
    print("\n4. УДАЛЯЕМ ТОВАР")
    cart_service.remove_from_cart(prod_id, "M")
    print(cart_service.get_cart_summary())
    
    print("\n5. ДОБАВЛЯЕМ СНОВА")
    cart_service.add_to_cart(prod_id, "L", 2)
    print(cart_service.get_cart_summary())
    
    print(f"\nИТОГО: {cart_service.get_total()} руб.")
    
    conn.close()