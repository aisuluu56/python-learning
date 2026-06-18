"""
Тесты для доменных моделей (01_domain_models)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_syntax_practice"))

from importlib import import_module

domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product
SizeStock = domain_models.SizeStock
Customer = domain_models.Customer


class TestCategory:
    def test_create_category(self):
        cat = Category(1, "Футболки", "Описание")
        assert cat.category_id == 1
        assert cat.name == "Футболки"

    def test_category_empty_name(self):
        with pytest.raises(ValueError):
            Category(1, "", "Описание")

    def test_category_negative_id(self):
        with pytest.raises(ValueError):
            Category(-1, "Футболки", "Описание")


class TestProduct:
    def test_create_product(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 1999, "Белый")
        assert product.product_id == 1
        assert product.name == "Футболка"

    def test_negative_price(self):
        cat = Category(1, "Футболки", "")
        with pytest.raises(ValueError):
            Product(1, "Футболка", cat, -100, "Белый")

    def test_empty_name(self):
        cat = Category(1, "Футболки", "")
        with pytest.raises(ValueError):
            Product(1, "", cat, 100, "Белый")

    def test_activate_deactivate(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        
        product.is_active = False
        assert product.is_active is False
        
        product.is_active = True
        assert product.is_active is True


class TestSizeStock:
    def test_create_stock(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        stock = SizeStock(product, "M", 10)
        assert stock.size == "M"
        assert stock.quantity == 10

    def test_negative_quantity(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        with pytest.raises(ValueError):
            SizeStock(product, "M", -5)

    def test_invalid_size(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        with pytest.raises(ValueError):
            SizeStock(product, "XXXL", 10)

    def test_add_stock(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        stock = SizeStock(product, "M", 10)
        stock.add_stock(5)
        assert stock.quantity == 15

    def test_remove_stock(self):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        stock = SizeStock(product, "M", 10)
        stock.remove_stock(3)
        assert stock.quantity == 7


class TestCustomer:
    def test_create_customer(self):
        customer = Customer(1, "Иван", "+79991234567", "ivan@mail.ru")
        assert customer.customer_id == 1
        assert customer.full_name == "Иван"

    def test_invalid_email(self):
        with pytest.raises(ValueError):
            Customer(1, "Иван", "+79991234567", "invalid")

    def test_empty_name(self):
        with pytest.raises(ValueError):
            Customer(1, "", "+79991234567", "ivan@mail.ru")


class TestParametrized:
    @pytest.mark.parametrize("size", ["XS", "S", "M", "L", "XL", "XXL"])
    def test_valid_sizes(self, size):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        stock = SizeStock(product, size, 10)
        assert stock.size == size

    @pytest.mark.parametrize("size", ["", "A", "42", "XXXL"])
    def test_invalid_sizes(self, size):
        cat = Category(1, "Футболки", "")
        product = Product(1, "Футболка", cat, 100, "Белый")
        with pytest.raises(ValueError):
            SizeStock(product, size, 10)