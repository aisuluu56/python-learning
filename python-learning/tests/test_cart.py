"""
Тесты для корзины
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_syntax_practice"))

from importlib import import_module

domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product

cart_module = import_module("17_clothing_store_project.05_cart.tasks")
Cart = cart_module.Cart
CartItem = cart_module.CartItem


@pytest.fixture
def category():
    return Category(1, "Футболки", "")


@pytest.fixture
def product(category):
    return Product(1, "Футболка", category, 100, "Белый")


@pytest.fixture
def cart():
    return Cart()


class TestCartItem:
    def test_create_item(self, product):
        """Создание позиции корзины"""
        item = CartItem(product, "M", 2)
        assert item.product == product
        assert item.size == "M"
        assert item.quantity == 2

    def test_item_total(self, product):
        """Сумма позиции"""
        item = CartItem(product, "M", 3)
        assert item.get_total() == 300


class TestCart:
    def test_add_item(self, cart, product):
        """Добавление товара"""
        cart.add_item(product, "M", 2)
        assert len(cart.items) == 1

    def test_add_same_item(self, cart, product):
        """Повторное добавление увеличивает количество"""
        cart.add_item(product, "M", 2)
        cart.add_item(product, "M", 3)
        assert cart.items[0].quantity == 5

    def test_different_sizes(self, cart, product):
        """Разные размеры - разные позиции"""
        cart.add_item(product, "M", 2)
        cart.add_item(product, "L", 3)
        assert len(cart.items) == 2

    def test_remove_item(self, cart, product):
        """Удаление позиции"""
        cart.add_item(product, "M", 2)
        cart.remove_item(product.product_id, "M")
        assert len(cart.items) == 0

    def test_update_quantity(self, cart, product):
        """Изменение количества"""
        cart.add_item(product, "M", 2)
        cart.update_quantity(product.product_id, "M", 5)
        assert cart.items[0].quantity == 5

    def test_update_quantity_to_zero(self, cart, product):
        """Изменение на 0 удаляет позицию"""
        cart.add_item(product, "M", 2)
        cart.update_quantity(product.product_id, "M", 0)
        assert len(cart.items) == 0

    def test_total_price(self, cart, product):
        """Общая сумма"""
        cart.add_item(product, "M", 2)
        assert cart.get_total() == 200

    def test_clear(self, cart, product):
        """Очистка корзины"""
        cart.add_item(product, "M", 2)
        cart.clear()
        assert len(cart.items) == 0

    def test_is_empty(self, cart):
        """Проверка пустой корзины"""
        assert cart.is_empty() is True
        cat = Category(1, "Футболки", "")
        prod = Product(1, "Футболка", cat, 100, "Белый")
        cart.add_item(prod, "M", 1)
        assert cart.is_empty() is False