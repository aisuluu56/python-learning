"""
Тесты для репозиториев (работа с базой данных)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module

domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product
SizeStock = domain_models.SizeStock
Customer = domain_models.Customer

repos_module = import_module("17_clothing_store_project.03_repositories.tasks")
CategoryRepository = repos_module.CategoryRepository
ProductRepository = repos_module.ProductRepository
StockRepository = repos_module.StockRepository
CustomerRepository = repos_module.CustomerRepository

db_module = import_module("17_clothing_store_project.02_postgresql_storage.tasks")
get_connection = db_module.get_connection


@pytest.fixture
def connection():
    conn = get_connection()
    yield conn
    conn.close()


def test_connection_works(connection):
    assert connection is not None


class TestCategoryRepository:
    def test_add_category(self, connection):
        repo = CategoryRepository(connection)
        cat = Category(None, "Футболки", "Мужские и женские")
        cat_id = repo.add(cat)
        assert cat_id > 0

    def test_get_category_by_id(self, connection):
        repo = CategoryRepository(connection)
        cat = Category(None, "Джинсы", "Классические")
        cat_id = repo.add(cat)
        found = repo.get_by_id(cat_id)
        assert found is not None
        assert found.name == "Джинсы"


class TestProductRepository:
    def test_add_product(self, connection):
        cat_repo = CategoryRepository(connection)
        cat = Category(None, "Обувь", "Кроссовки")
        cat_id = cat_repo.add(cat)
        cat = cat_repo.get_by_id(cat_id)
        
        repo = ProductRepository(connection)
        product = Product(None, "Кроссовки", cat, 5000, "Белый")
        prod_id = repo.add(product)
        assert prod_id > 0


class TestStockRepository:
    def test_add_stock(self, connection):
        cat_repo = CategoryRepository(connection)
        cat = Category(None, "Обувь", "")
        cat_id = cat_repo.add(cat)
        cat = cat_repo.get_by_id(cat_id)
        
        prod_repo = ProductRepository(connection)
        product = Product(None, "Кроссовки", cat, 5000, "Белый")
        prod_id = prod_repo.add(product)
        product = prod_repo.get_by_id(prod_id)
        
        repo = StockRepository(connection)
        stock = SizeStock(product, "M", 10)
        repo.add(stock)
        
        quantity = repo.get_quantity(prod_id, "M")
        assert quantity == 10


class TestCustomerRepository:
    def test_add_customer(self, connection):
        repo = CustomerRepository(connection)
        customer = Customer(None, "Иван Петров", "+79991234567", "ivan@mail.ru")
        cust_id = repo.add(customer)
        assert cust_id > 0