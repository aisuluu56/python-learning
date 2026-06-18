"""
Этап 04. Сервис каталога

Цель: вынести логику просмотра, поиска и фильтрации товаров в отдельный
сервисный слой.

Сервис каталога создавайте прямо в этом файле.
Репозитории импортируйте из 03_repositories/tasks.py.
"""

from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Задание 1
# Импортируйте модели, репозитории товаров, категорий и остатков по размерам.
# Добавьте несколько товаров разных категорий, цветов, размеров, цен и остатков.

# TODO: подготовить данные каталога

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

db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


# Задание 2
# Создайте сервис каталога, который получает репозиторий товаров.
# При необходимости передайте в сервис репозиторий категорий и репозиторий остатков.
# Сервис должен работать через методы репозиториев, а не через внешний список.

# TODO: добавить сервис каталога

class CatalogService:
    def __init__(self, product_repo, category_repo=None, stock_repo=None):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.stock_repo = stock_repo


# Задание 3
# Добавьте получение активных товаров.
# Неактивные товары не должны попадать в обычную выдачу каталога.

# TODO: добавить выдачу активных товаров

    def get_active_products(self):
        all_products = self.product_repo.get_all()
        active_products = []
        for product in all_products:
            if product.is_active:
                active_products.append(product)
        return active_products


# Задание 4
# Добавьте поиск по части названия.
# Поиск должен быть удобным для пользователя и не зависеть от регистра.

# TODO: добавить поиск по названию

    def search_by_name(self, query):
        if not query or not query.strip():
            return []
        
        products = self.get_active_products()
        found = []
        query_lower = query.lower().strip()
        
        for product in products:
            if query_lower in product.name.lower():
                found.append(product)
        return found


# Задание 5
# Добавьте фильтрацию по категории, размеру, цвету и диапазону цены.
# Фильтр по размеру должен учитывать наличие товара именно этого размера.
# Фильтры можно реализовать постепенно.

# TODO: добавить фильтрацию каталога

    def filter_by_category(self, category_id):
        products = self.get_active_products()
        filtered = []
        for product in products:
            if product.category.category_id == category_id:
                filtered.append(product)
        return filtered

    def filter_by_color(self, color):
        if not color or not color.strip():
            return []
        
        products = self.get_active_products()
        filtered = []
        color_lower = color.lower().strip()
        
        for product in products:
            if product.color.lower() == color_lower:
                filtered.append(product)
        return filtered

    def filter_by_price(self, min_price=None, max_price=None):
        products = self.get_active_products()
        filtered = []
        
        for product in products:
            if min_price is not None and product.price < min_price:
                continue
            if max_price is not None and product.price > max_price:
                continue
            filtered.append(product)
        return filtered

    def filter_by_size(self, size):
        if not size or not size.strip():
            return []
        
        products = self.get_active_products()
        filtered = []
        size_upper = size.upper().strip()
        
        for product in products:
            if self.stock_repo:
                quantity = self.stock_repo.get_quantity(product.product_id, size_upper)
                if quantity > 0:
                    filtered.append(product)
        return filtered


# Задание 6
# Добавьте сортировку найденных товаров.
# Продумайте варианты сортировки по цене и названию.

# TODO: добавить сортировку каталога

    def sort_products(self, products, sort_by='price', reverse=False):
        if not products:
            return []
        
        if sort_by == 'price':
            return sorted(products, key=lambda x: x.price, reverse=reverse)
        elif sort_by == 'name':
            return sorted(products, key=lambda x: x.name.lower(), reverse=reverse)
        return products


# Задание 7
# Проверьте сервис на нескольких сценариях поиска и фильтрации.

# TODO: добавить ручную проверку сервиса каталога

if __name__ == "__main__":
    conn = get_connection()
    
    category_repo = CategoryRepository(conn)
    product_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    
    catalog = CatalogService(product_repo, category_repo, stock_repo)
    
    active = catalog.get_active_products()
    print(f"Активных товаров: {len(active)}")
    
    found = catalog.search_by_name("футболка")
    print(f"Найдено по запросу 'футболка': {len(found)}")
    
    by_price = catalog.filter_by_price(min_price=1000, max_price=3000)
    print(f"Товаров от 1000 до 3000 руб: {len(by_price)}")
    
    sorted_products = catalog.sort_products(active, sort_by='price', reverse=True)
    print("Отсортировано по цене (дорогие сначала)")
    
    conn.close()