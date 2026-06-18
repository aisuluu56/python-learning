"""
Тема 15. property и сеттеры
"""


# Задание 1
# Создайте класс CourseProgress.
# В __init__ принимайте student_name и percent.
# Храните процент выполнения во внутреннем атрибуте _percent.
# Добавьте property percent, который возвращает _percent.
# Создайте объект и выведите progress.percent.

# TODO: решение
class CourseProgress:
    def __init__(self, student_name, percent):
        self.student_name = student_name
        self._percent = percent

    @property
    def percent(self):
        return self._percent


progress = CourseProgress("Анна", 75)
print(f"Прогресс {progress.student_name}: {progress.percent}%")
print()


# Задание 2
# Добавьте в CourseProgress сеттер для percent.
# Процент не может быть меньше 0 или больше 100.
# В __init__ используйте self.percent = percent, чтобы начальное значение тоже проходило проверку.

# TODO: решение
class CourseProgress:
    def __init__(self, student_name, percent):
        self.student_name = student_name
        self.percent = percent  # Используем сеттер для проверки

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        if value < 0 or value > 100:
            raise ValueError("Процент должен быть от 0 до 100")
        self._percent = value


progress = CourseProgress("Анна", 75)
print(f"Прогресс: {progress.percent}%")
progress.percent = 90
print(f"Новый прогресс: {progress.percent}%")

try:
    progress.percent = 150
except ValueError as e:
    print(f"Ошибка: {e}")
print()


# Задание 3
# Создайте класс Passport.
# В __init__ принимайте number.
# Храните номер во внутреннем атрибуте _number.
# Добавьте property number без сеттера.
# Проверьте, что номер можно прочитать через passport.number.

# TODO: решение
class Passport:
    def __init__(self, number):
        self._number = number

    @property
    def number(self):
        return self._number


passport = Passport("1234 567890")
print(f"Номер паспорта: {passport.number}")

try:
    passport.number = "9999 111111"  # Должно вызвать ошибку
except AttributeError as e:
    print(f"Нельзя изменить номер: {e}")
print()


# Задание 4
# Создайте класс Circle.
# В __init__ принимайте radius.
# Добавьте property diameter, который возвращает диаметр.
# Добавьте property area, который возвращает площадь круга.
# Для числа pi можно использовать 3.14.

# TODO: решение
class Circle:
    pi = 3.14

    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return self.pi * self.radius ** 2


circle = Circle(5)
print(f"Радиус: {circle.radius}")
print(f"Диаметр: {circle.diameter}")
print(f"Площадь: {circle.area:.2f}")

# Диаметр и площадь вычисляются автоматически при изменении радиуса
circle.radius = 10
print(f"\nПосле увеличения радиуса до {circle.radius}:")
print(f"Диаметр: {circle.diameter}")
print(f"Площадь: {circle.area:.2f}")
print()


# Задание 5
# Создайте класс StorageBox.
# Внутри храните _items_count.
# Добавьте property items_count только для чтения.
# Добавьте методы add_items(count) и remove_items(count).
# Нельзя добавлять или убирать количество меньше или равное 0.
# Нельзя убрать больше предметов, чем есть в коробке.

# TODO: решение
class StorageBox:
    def __init__(self, initial_count=0):
        if initial_count < 0:
            raise ValueError("Начальное количество не может быть отрицательным")
        self._items_count = initial_count

    @property
    def items_count(self):
        return self._items_count

    def add_items(self, count):
        if count <= 0:
            raise ValueError("Количество для добавления должно быть положительным")
        self._items_count += count
        print(f"Добавлено {count} предметов. Всего: {self._items_count}")

    def remove_items(self, count):
        if count <= 0:
            raise ValueError("Количество для удаления должно быть положительным")
        if count > self._items_count:
            raise ValueError(f"Недостаточно предметов. Есть {self._items_count}, запрошено {count}")
        self._items_count -= count
        print(f"Удалено {count} предметов. Осталось: {self._items_count}")


box = StorageBox(10)
print(f"Предметов в коробке: {box.items_count}")

box.add_items(5)
box.remove_items(3)

try:
    box.remove_items(20)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    box.items_count = 100  # Должно вызвать ошибку
except AttributeError as e:
    print(f"Нельзя изменить напрямую: {e}")
print()


# Задание 6
# Создайте класс Speed.
# Внутри храните скорость в километрах в час.
# Добавьте property kmh с сеттером.
# Скорость не может быть отрицательной.
# Добавьте property ms, который возвращает скорость в метрах в секунду по формуле:
# kmh / 3.6

# TODO: решение
class Speed:
    def __init__(self, kmh=0):
        self.kmh = kmh  # Используем сеттер

    @property
    def kmh(self):
        return self._kmh

    @kmh.setter
    def kmh(self, value):
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self._kmh = value

    @property
    def ms(self):
        return self._kmh / 3.6


speed = Speed(72)
print(f"Скорость: {speed.kmh} км/ч")
print(f"Скорость: {speed.ms:.2f} м/с")

speed.kmh = 108
print(f"\nНовая скорость: {speed.kmh} км/ч")
print(f"Новая скорость: {speed.ms:.2f} м/с")

try:
    speed.kmh = -50
except ValueError as e:
    print(f"\nОшибка: {e}")
print()


# Дополнительная демонстрация всех возможностей
print("=" * 50)
print("ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ")
print("=" * 50)


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance  # Используем сеттер

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = value

    @property
    def is_positive(self):
        return self._balance > 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount


account = BankAccount("Иван", 1000)
print(f"{account.owner}: баланс = {account.balance} руб.")
print(f"Баланс положительный? {account.is_positive}")

account.deposit(500)
print(f"После пополнения: {account.balance} руб.")

account.withdraw(300)
print(f"После снятия: {account.balance} руб.")