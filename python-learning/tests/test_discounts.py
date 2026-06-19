"""
Тесты для скидок и промокодов
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module

user_module = import_module("17_clothing_store_project.07_users_discounts.tasks")
Promocode = user_module.Promocode
DiscountService = user_module.DiscountService


@pytest.fixture
def discount_service():
    """Создает сервис с тестовыми промокодами"""
    class FakePromoRepo:
        def __init__(self):
            self.promos = [
                Promocode("SALE10", 10, 0),        # 10% скидка без минимума
                Promocode("SALE20", 20, 1000),      # 20% скидка от 1000 руб
                Promocode("SALE30", 30, 5000),      # 30% скидка от 5000 руб
            ]
        
        def get_by_code(self, code):
            for p in self.promos:
                if p.code == code:
                    return p
            return None
    
    return DiscountService(FakePromoRepo())


class TestDiscounts:
    def test_valid_promocode(self, discount_service):
        """Валидный промокод применяется"""
        result = discount_service.apply_promocode(1000, "SALE10")
        assert result == 900  # 1000 - 10% = 900

    def test_promocode_with_min_order(self, discount_service):
        """Промокод с минимальной суммой"""
        # Сумма достаточная
        result = discount_service.apply_promocode(1500, "SALE20")
        assert result == 1200  # 1500 - 20% = 1200

    def test_promocode_min_order_not_met(self, discount_service):
        """Ошибка если сумма меньше минимальной"""
        with pytest.raises(ValueError):
            discount_service.apply_promocode(500, "SALE20")  # минимум 1000

    def test_unknown_promocode(self, discount_service):
        """Неизвестный промокод вызывает ошибку"""
        with pytest.raises(ValueError):
            discount_service.apply_promocode(1000, "UNKNOWN")

    def test_promocode_with_zero_discount(self, discount_service):
        """Промокод с 0% скидки"""
        class FakeRepo:
            def get_by_code(self, code):
                return Promocode("ZERO", 0, 0)
        
        service = DiscountService(FakeRepo())
        result = service.apply_promocode(1000, "ZERO")
        assert result == 1000  # цена не меняется

    def test_different_discounts(self, discount_service):
        """Разные промокоды дают разную скидку"""
        # 10% скидка
        result1 = discount_service.apply_promocode(1000, "SALE10")
        assert result1 == 900
        
        # 20% скидка (если сумма подходит)
        result2 = discount_service.apply_promocode(1000, "SALE20")
        assert result2 == 800