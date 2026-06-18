"""
Тема 16. classmethod и staticmethod
"""


# Задание 1
# Создайте класс Employee с атрибутами name и position.
# Добавьте обычный метод get_info(), который возвращает строку с именем и должностью.

# TODO: решение
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_info(self):
        return f"Сотрудник: {self.name}, Должность: {self.position}"


emp = Employee("Анна", "Разработчик")
print(emp.get_info())
print()


# Задание 2
# Добавьте в Employee метод класса from_dict(data).
# Он должен создавать сотрудника из словаря:
# {"name": ..., "position": ...}

# TODO: решение
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_info(self):
        return f"Сотрудник: {self.name}, Должность: {self.position}"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["position"])


data = {"name": "Иван", "position": "Менеджер"}
emp = Employee.from_dict(data)
print(emp.get_info())
print()


# Задание 3
# Создайте класс Song с атрибутами title и duration.
# Добавьте метод класса from_string(text).
# Строка приходит в формате:
# title;duration
# Например: "Imagine;183"

# TODO: решение
class Song:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    def __str__(self):
        return f"Песня: {self.title}, Длительность: {self.duration} сек."

    @classmethod
    def from_string(cls, text):
        title, duration = text.split(";")
        return cls(title, int(duration))


song = Song.from_string("Imagine;183")
print(song)
print()


# Задание 4
# Создайте класс TextHelper.
# Добавьте staticmethod is_short(text), который возвращает True,
# если длина строки меньше 10, и False иначе.
# Проверьте метод без создания объекта.

# TODO: решение
class TextHelper:
    @staticmethod
    def is_short(text):
        return len(text) < 10


print(f"Hello: {TextHelper.is_short('Hello')}")        # True (5 < 10)
print(f"Hello World: {TextHelper.is_short('Hello World')}")  # False (11 >= 10)
print()


# Задание 5
# Создайте класс Password.
# В __init__ принимайте value.
# Добавьте staticmethod is_strong(value), который проверяет,
# что длина пароля не меньше 8.
# Если пароль слишком короткий, выбрасывайте ValueError.

# TODO: решение
class Password:
    def __init__(self, value):
        if not self.is_strong(value):
            raise ValueError("Пароль слишком короткий! Должен быть не менее 8 символов.")
        self.value = value

    @staticmethod
    def is_strong(value):
        return len(value) >= 8


# Успешное создание
pwd = Password("secure123")
print("Пароль создан успешно!")

# Неудачное создание
try:
    pwd2 = Password("weak")
except ValueError as e:
    print(f"Ошибка: {e}")
print()


# Задание 6
# Создайте класс Time.
# В __init__ принимайте hours и minutes.
# Добавьте classmethod from_string(text).
# Строка приходит в формате:
# "09:30"
# Метод должен вернуть объект Time.
# Добавьте __str__(), чтобы время красиво выводилось через print().

# TODO: решение
class Time:
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    @classmethod
    def from_string(cls, text):
        hours, minutes = text.split(":")
        return cls(int(hours), int(minutes))

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}"


time1 = Time(9, 30)
print(f"Время: {time1}")

time2 = Time.from_string("14:45")
print(f"Время из строки: {time2}")

time3 = Time.from_string("08:05")
print(f"Время из строки: {time3}")
print()


# Дополнительная демонстрация всех трех видов методов
print("=" * 50)
print("ДЕМОНСТРАЦИЯ ТРЕХ ВИДОВ МЕТОДОВ")
print("=" * 50)


class User:
    count = 0

    def __init__(self, name, email):
        self.name = name
        self.email = email
        User.count += 1

    # Обычный метод (self - объект)
    def get_info(self):
        return f"{self.name} ({self.email})"

    # Метод класса (cls - класс)
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])

    @classmethod
    def get_count(cls):
        return f"Всего пользователей: {cls.count}"

    # Статический метод (ни self, ни cls)
    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email


# Создание объектов разными способами
user1 = User("Анна", "anna@example.com")
user2 = User.from_dict({"name": "Иван", "email": "ivan@example.com"})

print(f"user1: {user1.get_info()}")
print(f"user2: {user2.get_info()}")

# Метод класса
print(User.get_count())

# Статический метод
print(f"is_valid_email('test@mail.ru'): {User.is_valid_email('test@mail.ru')}")
print(f"is_valid_email('invalid'): {User.is_valid_email('invalid')}")
print()


# Еще пример: альтернативные конструкторы
print("=" * 50)
print("АЛЬТЕРНАТИВНЫЕ КОНСТРУКТОРЫ")
print("=" * 50)


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, text):
        # Формат: "2024-12-25"
        year, month, day = map(int, text.split("-"))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        # Альтернативный конструктор с текущей датой
        from datetime import datetime
        now = datetime.now()
        return cls(now.year, now.month, now.day)

    def __str__(self):
        return f"{self.day:02d}.{self.month:02d}.{self.year}"


date1 = Date(2025, 6, 8)
print(f"Дата: {date1}")

date2 = Date.from_string("2025-12-25")
print(f"Дата из строки: {date2}")

date3 = Date.today()
print(f"Сегодняшняя дата: {date3}")