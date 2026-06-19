"""
Этап 01. Доменные модели магазина одежды

Цель: описать основные объекты предметной области без подключения к БД,
меню, репозиториев и сервисов.

Модели создавайте прямо в этом файле. Следующие этапы будут импортировать
их отсюда, а не копировать классы заново.
"""


# Задание 1
# Опишите модель категории одежды.
# Категория должна хранить идентификатор, название и краткое описание.

# TODO: добавить модель категории
class Category:
    def __init__(self, category_id, name, description):
        if category_id is not None and category_id <= 0:
            raise ValueError("ID категории должен быть положительным")
        #if not name or not name.strip():
            #raise ValueError("Название категории не может быть пустым")
        
        self.category_id = category_id
        self.name = name.strip()
        self.description = description.strip() if description else ""


# Задание 2
# Опишите модель товара.
# Продумайте поля для идентификатора, названия, категории, цены, цвета,
# описания и активности товара.

# TODO: добавить модель товара
class Product:
    def __init__(self, product_id, name, category, price, color, description="", is_active=True):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.color = color
        self.description = description
        self.is_active = is_active


# Задание 3
# Добавьте проверки для данных товара.
# Обратите внимание на цену, пустое название и связь с категорией.

# TODO: добавить защиту состояния товара
class Product:
    def __init__(self, product_id, name, category, price, color, description="", is_active=True):
        if product_id is not None and product_id <= 0:
            raise ValueError("ID товара должен быть положительным")
        if not name or not name.strip():
            raise ValueError("Название товара не может быть пустым")
        if not isinstance(category, Category):
            raise ValueError("Категория должна быть объектом Category")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if not color or not color.strip():
            raise ValueError("Цвет товара не может быть пустым")
        
        self.product_id = product_id
        self.name = name.strip()
        self.category = category
        self.price = price
        self.color = color.strip()
        self.description = description.strip() if description else ""
        self.is_active = is_active
        self._sizes_stock = {}


# Задание 4
# Опишите модель остатка товара по размеру.
# Она должна связывать товар, размер и количество этого размера на складе.

# TODO: добавить модель остатка по размеру
class SizeStock:
    VALID_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
    
    def __init__(self, product, size, quantity):
        if not isinstance(product, Product):
            raise ValueError("Должен быть указан объект Product")
        if size not in self.VALID_SIZES:
            raise ValueError(f"Размер должен быть из {self.VALID_SIZES}")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        
        self.product = product
        self.size = size
        self._quantity = quantity


# Задание 5
# Добавьте поведение товара.
# Товар или отдельная модель остатка должны помогать понять,
# доступен ли конкретный размер и какое количество можно купить.

# TODO: добавить методы изменения и проверки товара
class Product:
    def __init__(self, product_id, name, category, price, color, description="", is_active=True):
        if product_id is not None and product_id <= 0:
            raise ValueError("ID товара должен быть положительным")
        if not name or not name.strip():
            raise ValueError("Название товара не может быть пустым")
        #if not isinstance(category, Category):
            #raise ValueError("Категория должна быть объектом Category")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if not color or not color.strip():
            raise ValueError("Цвет товара не может быть пустым")
        
        self.product_id = product_id
        self.name = name.strip()
        self.category = category
        self.price = price
        self.color = color.strip()
        self.description = description.strip() if description else ""
        self.is_active = is_active
        self._sizes_stock = {}

    def add_size_stock(self, size, quantity):
        if size in self._sizes_stock:
            self._sizes_stock[size].add_stock(quantity)
        else:
            self._sizes_stock[size] = SizeStock(self, size, quantity)

    def is_size_available(self, size, quantity=1):
        stock = self._sizes_stock.get(size)
        return stock and stock.is_available(quantity) and self.is_active

    def get_available_sizes(self):
        return [size for size, stock in self._sizes_stock.items() if stock.is_available()]


class SizeStock:
    VALID_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
    
    def __init__(self, product, size, quantity):
        #if not isinstance(product, Product):
            #raise ValueError("Должен быть указан объект Product")
        if size not in self.VALID_SIZES:
            raise ValueError(f"Размер должен быть из {self.VALID_SIZES}")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        
        self.product = product
        self.size = size
        self._quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    def add_stock(self, amount):
        if amount <= 0:
            raise ValueError("Количество для добавления должно быть положительным")
        self._quantity += amount

    def remove_stock(self, amount):
        if amount <= 0:
            raise ValueError("Количество для удаления должно быть положительным")
        if amount > self._quantity:
            raise ValueError(f"Недостаточно товара. Доступно: {self._quantity}")
        self._quantity -= amount

    def is_available(self, requested_quantity=1):
        return self._quantity >= requested_quantity and self.product.is_active


# Задание 6
# Опишите модель покупателя.
# Продумайте поля для идентификатора, имени, телефона и email.

# TODO: добавить модель покупателя
class Customer:
    def __init__(self, customer_id, full_name, phone, email):
        if customer_id is not None and customer_id <= 0:
            raise ValueError("ID покупателя должен быть положительным")
        if not full_name or not full_name.strip():
            raise ValueError("Имя покупателя не может быть пустым")
        if not phone or not phone.strip():
            raise ValueError("Телефон не может быть пустым")
        if not email or "@" not in email or "." not in email:
            raise ValueError("Некорректный email адрес")
        
        self.customer_id = customer_id
        self.full_name = full_name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self._order_history = []

    def add_to_order_history(self, order):
        self._order_history.append(order)

    def get_order_history(self):
        return self._order_history.copy()


# Задание 7
# Создайте несколько объектов и проверьте, что корректные данные принимаются,
# а некорректные приводят к понятной ошибке.

# TODO: добавить ручную проверку моделей
if __name__ == "__main__":
    category = Category(1, "Футболки", "Мужские и женские футболки")
    product = Product(1, "Classic T-Shirt", category, 1999, "Белый")
    product.add_size_stock("M", 10)
    product.add_size_stock("L", 5)
    
    print(product.is_size_available("M", 2))
    print(product.get_available_sizes())
    
    customer = Customer(1, "Иванов Иван", "+7(999)123-45-67", "ivan@example.com")
    print(customer.full_name)