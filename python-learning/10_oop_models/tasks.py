"""
Тема 10. Классы-модели
"""


# Задание 1
# Создайте модель User.
# Атрибуты: name, email, age.
# Добавьте метод get_info(), который возвращает строку с данными пользователя.

# TODO: решение
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Email: {self.email}"


# Задание 2
# Добавьте в User валидацию возраста.
# Если age меньше 0, выбрасывайте ValueError.

# TODO: решение
class User:
    def __init__(self, name, email, age):
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным!")
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Email: {self.email}"


# Задание 3
# Создайте модель Product.
# Атрибуты: title, price, count.
# Добавьте метод get_total_price(), который возвращает price * count.
# Добавьте проверку: price и count не могут быть отрицательными.

# TODO: решение
class Product:
    def __init__(self, title, price, count):
        if price < 0 or count < 0:
            raise ValueError("Цена и количество не могут быть отрицательными!")
        self.title = title
        self.price = price
        self.count = count

    def get_total_price(self):
        return self.price * self.count
    
    def __repr__(self):
        return f"Товар: {self.title}, цена: {self.price}, кол-во: {self.count}"


# Задание 4
# Создайте модель Task.
# Атрибуты: title, is_done.
# При создании is_done должен быть False.
# Добавьте методы mark_done() и mark_undone().

# TODO: решение
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True

    def mark_undone(self):
        self.is_done = False


# Задание 5
# Добавьте в Task метод to_dict().
# Он должен возвращать словарь:
# {"title": ..., "is_done": ...}

# TODO: решение
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True

    def mark_undone(self):
        self.is_done = False

    def to_dict(self):
        return {"title": self.title, "is_done": self.is_done}


# Задание 6
# Создайте модель Order.
# Атрибуты: customer_name, products.
# products — список объектов Product.
# Добавьте метод get_total(), который возвращает сумму всех товаров.

# TODO: решение
class Order:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_total(self):
        total = 0
        for product in self.products:
            total += product.get_total_price()
        return total

order = Order("Максим")
product1 = Product("Молоко", 67.75, 1)
product2 = Product("Чай", 404.56, 1)
product3 = Product("Сахар", 30.25, 3)
order.add_product(product1)
order.add_product(product2)
order.add_product(product3)
print(order.get_total())
print(order.products)