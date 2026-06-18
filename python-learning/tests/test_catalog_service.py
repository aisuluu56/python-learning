"""
Тесты для сервиса каталога
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_syntax_practice"))

from importlib import import_module

domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product

catalog_module = import_module("17_clothing_store_project.04_catalog_service.tasks")
CatalogService = catalog_module.CatalogService


@pytest.fixture
def catalog_service():
    """Создает сервис с тестовыми товарами"""
    class FakeRepo:
        def get_all(self):
            cat1 = Category(1, "Футболки", "")
            cat2 = Category(2, "Джинсы", "")
            return [
                Product(1, "Белая футболка", cat1, 1000, "Белый", "", True),
                Product(2, "Синяя футболка", cat1, 1500, "Синий", "", True),
                Product(3, "Черная футболка", cat1, 2000, "Черный", "", True),
                Product(4, "Джинсы", cat2, 3000, "Синий", "", True),
                Product(5, "Старая футболка", cat1, 500, "Белый", "", False),
            ]
        
        def get_by_category(self, category_id):
            return [p for p in self.get_all() if p.category.category_id == category_id]
    
    return CatalogService(FakeRepo())


class TestCatalog:
    def test_active_products(self, catalog_service):
        """Только активные товары"""
        products = catalog_service.get_active_products()
        assert len(products) == 4  # 5 всего, 1 неактивный

    def test_search(self, catalog_service):
        """Поиск по названию"""
        result = catalog_service.search_by_name("футболка")
        assert len(result) == 3  # 3 футболки

    def test_filter_category(self, catalog_service):
        """Фильтр по категории"""
        result = catalog_service.filter_by_category(1)
        assert len(result) == 3  # футболки

    def test_filter_color(self, catalog_service):
        """Фильтр по цвету"""
        result = catalog_service.filter_by_color("Белый")
        assert len(result) == 1

    def test_filter_price(self, catalog_service):
        """Фильтр по цене"""
        result = catalog_service.filter_by_price(1000, 2000)
        assert len(result) == 3

    def test_sort_price(self, catalog_service):
        """Сортировка по цене"""
        products = catalog_service.get_active_products()
        sorted_products = catalog_service.sort_products(products, "price")
        prices = [p.price for p in sorted_products]
        assert prices == [1000, 1500, 2000, 3000]