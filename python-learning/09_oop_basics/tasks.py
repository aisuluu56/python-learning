"""
Тема 9. Основы ООП: классы и объекты
"""


# Задание 1
# Создайте класс Student.
# В __init__ сохраните name и age.
# Создайте объект и выведите его имя и возраст.

# TODO: решение
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


student1 = Student("Алексей", 17)
print(student1.name)
print(student1.age)


# Задание 2
# Добавьте в класс Student метод greet().
# Метод должен возвращать строку:
# Привет, меня зовут <name>.

# TODO: решение
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Привет, меня зовут {self.name}."


student2 = Student("Мария", 16)
print(student2.greet())


# Задание 3
# Создайте класс Product с атрибутами title и price.
# Добавьте метод get_info(), который возвращает строку:
# <title>: <price> руб.

# TODO: решение
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def get_info(self):
        return f"{self.title}: {self.price} руб."


product = Product("Ноутбук", 65000)
print(product.get_info())


# Задание 4
# Создайте класс Rectangle с атрибутами width и height.
# Добавьте метод area(), который возвращает площадь.
# Добавьте метод perimeter(), который возвращает периметр.

# TODO: решение
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


rect = Rectangle(10, 5)
print("Площадь:", rect.area())
print("Периметр:", rect.perimeter())


# Задание 5
# Создайте класс BankAccount.
# Внутри храните owner и balance.
# Добавьте методы deposit(amount) и withdraw(amount).
# deposit увеличивает баланс.
# withdraw уменьшает баланс, если денег достаточно.

# TODO: решение
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Пополнение: +{amount}. Баланс: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Снятие: -{amount}. Баланс: {self.balance}")
        else:
            print("Недостаточно средств!")


account = BankAccount("Иван", 1000)
account.deposit(500)
account.withdraw(300)
account.withdraw(2000)


# Задание 6
# Создайте несколько объектов Student и положите их в список.
# С помощью цикла выведите информацию о каждом студенте.

# TODO: решение
students = [
    Student("Алексей", 17),
    Student("Мария", 16),
    Student("Дмитрий", 18)
]

print("\nСписок студентов:")
for s in students:
    print(f"Имя: {s.name}, Возраст: {s.age}")