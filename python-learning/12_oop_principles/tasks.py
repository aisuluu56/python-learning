"""
Тема 12. Основные принципы ООП
"""


# Задание 1. Инкапсуляция
# Создайте класс BankAccount.
# Внутри храните _owner и _balance.
# Добавьте методы:
# deposit(amount)
# withdraw(amount)
# get_balance()
# Нельзя пополнять или снимать сумму меньше или равную 0.
# Нельзя снять больше, чем есть на балансе.

# TODO: решение
class BankAccount:
    def __init__(self, owner, balance=0):
        self._owner = owner
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount
        return f"Пополнено: {amount}. Баланс: {self._balance}"

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        return f"Снято: {amount}. Баланс: {self._balance}"

    def get_balance(self):
        return self._balance


# Задание 2. Инкапсуляция в модели
# Создайте класс Product.
# Внутри храните _title и _price.
# Добавьте метод set_price(price), который меняет цену.
# Цена не может быть отрицательной.
# Добавьте метод get_info(), который возвращает строку с названием и ценой.

# TODO: решение
class Product:
    def __init__(self, title, price):
        self._title = title
        self._price = price

    def set_price(self, price):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = price

    def get_info(self):
        return f"Товар: {self._title}, Цена: {self._price} руб."


# Задание 3. Наследование
# Создайте класс User с атрибутом name и методом get_role().
# get_role() должен возвращать "user".
# Создайте класс Admin, который наследуется от User.
# Переопределите get_role(), чтобы он возвращал "admin".

# TODO: решение
class User:
    def __init__(self, name):
        self.name = name

    def get_role(self):
        return "user"


class Admin(User):
    def get_role(self):
        return "admin"


# Задание 4. Наследование и расширение поведения
# Создайте класс Employee с атрибутами name и salary.
# Добавьте метод get_info().
# Создайте класс Manager, который наследуется от Employee.
# Добавьте Manager атрибут department.
# Переопределите get_info(), чтобы он возвращал имя, зарплату и отдел.

# TODO: решение
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_info(self):
        return f"Сотрудник: {self.name}, Зарплата: {self.salary} руб."


class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department

    def get_info(self):
        return f"Менеджер: {self.name}, Зарплата: {self.salary} руб., Отдел: {self.department}"


# Задание 5. Полиморфизм
# Создайте классы EmailNotifier и SmsNotifier.
# В каждом классе должен быть метод send(message).
# EmailNotifier возвращает строку "Email: <message>".
# SmsNotifier возвращает строку "SMS: <message>".
# Создайте функцию notify(notifier, message), которая вызывает notifier.send(message).
# Проверьте функцию с объектами обоих классов.

# TODO: решение
class EmailNotifier:
    def send(self, message):
        return f"Email: {message}"


class SmsNotifier:
    def send(self, message):
        return f"SMS: {message}"


def notify(notifier, message):
    return notifier.send(message)


# Задание 6. Абстракция
# Создайте классы MemoryStorage и ConsoleStorage.
# У каждого должен быть метод save(item).
# MemoryStorage сохраняет элементы в список.
# ConsoleStorage выводит элемент на экран.
# Создайте функцию save_item(storage, item), которая вызывает storage.save(item).
# Проверьте функцию с обоими хранилищами.

# TODO: решение
class MemoryStorage:
    def __init__(self):
        self.items = []

    def save(self, item):
        self.items.append(item)
        return f"Сохранено в память: {item}"


class ConsoleStorage:
    def save(self, item):
        print(f"Вывод в консоль: {item}")
        return f"Выведено в консоль: {item}"


def save_item(storage, item):
    return storage.save(item)


# Задание 7. Композиция
# Создайте класс Engine с методом start().
# Метод возвращает "Двигатель запущен".
# Создайте класс Car.
# Внутри Car должен храниться объект Engine.
# Метод Car.start() должен запускать двигатель и возвращать результат.

# TODO: решение
class Engine:
    def start(self):
        return "Двигатель запущен"


class Car:
    def __init__(self, model):
        self.model = model
        self.engine = Engine()

    def start(self):
        return f"{self.model}: {self.engine.start()}"


# Проверка всех заданий
if __name__ == "__main__":
    print("=" * 50)
    print("ЗАДАНИЕ 1 - BankAccount")
    print("=" * 50)
    account = BankAccount("Иван", 1000)
    print(account.deposit(500))
    print(account.withdraw(300))
    print(f"Баланс: {account.get_balance()}")
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 2 - Product")
    print("=" * 50)
    product = Product("Ноутбук", 50000)
    print(product.get_info())
    product.set_price(45000)
    print(product.get_info())
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 3 - User/Admin")
    print("=" * 50)
    user = User("Алексей")
    admin = Admin("Мария")
    print(f"{user.name}: {user.get_role()}")
    print(f"{admin.name}: {admin.get_role()}")
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 4 - Employee/Manager")
    print("=" * 50)
    emp = Employee("Дмитрий", 50000)
    mgr = Manager("Анна", 80000, "IT")
    print(emp.get_info())
    print(mgr.get_info())
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 5 - Полиморфизм")
    print("=" * 50)
    email_notifier = EmailNotifier()
    sms_notifier = SmsNotifier()
    print(notify(email_notifier, "Ваш заказ подтвержден"))
    print(notify(sms_notifier, "Ваш заказ подтвержден"))
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 6 - Абстракция")
    print("=" * 50)
    memory = MemoryStorage()
    console = ConsoleStorage()
    print(save_item(memory, "Книга"))
    print(save_item(memory, "Ручка"))
    save_item(console, "Монитор")
    save_item(console, "Клавиатура")
    print(f"В памяти сохранено: {memory.items}")
    print()

    print("=" * 50)
    print("ЗАДАНИЕ 7 - Композиция")
    print("=" * 50)
    car = Car("Tesla Model 3")
    print(car.start())