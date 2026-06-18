# Тема 12. Основные принципы ООП

## Что такое принципы ООП

ООП — это не только синтаксис классов.

Основные принципы ООП помогают проектировать код так, чтобы его было проще расширять, проверять и поддерживать.

Обычно выделяют четыре принципа:

- инкапсуляция;
- наследование;
- полиморфизм;
- абстракция.

## 1. Инкапсуляция

Инкапсуляция означает, что объект хранит данные внутри себя и сам управляет тем, как эти данные меняются.

Плохой вариант: любой код напрямую меняет баланс.

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance


account = BankAccount(1000)
account.balance = -500
```

Формально код работает, но счет оказался в неправильном состоянии.

Лучше менять данные через методы:

```python
class BankAccount:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")

        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        if amount > self._balance:
            raise ValueError("Недостаточно средств")

        self._balance -= amount

    def get_balance(self):
        return self._balance
```

Одинарное подчеркивание в `_balance` — договоренность: этот атрибут считается внутренним, его не стоит менять напрямую снаружи.

## 2. Наследование

Наследование позволяет создать новый класс на основе существующего.

```python
class User:
    def __init__(self, name):
        self.name = name

    def get_info(self):
        return f"Пользователь: {self.name}"


class Admin(User):
    def ban_user(self, user):
        return f"{self.name} заблокировал {user.name}"
```

`Admin` наследует атрибуты и методы `User`.

```python
admin = Admin("Anna")
print(admin.get_info())
```

## Переопределение методов

Дочерний класс может изменить поведение метода родителя.

```python
class User:
    def get_role(self):
        return "user"


class Admin(User):
    def get_role(self):
        return "admin"
```

Метод называется одинаково, но работает по-разному.

## 3. Полиморфизм

Полиморфизм означает, что разные объекты могут использоваться одинаковым способом, если у них есть общий метод.

```python
class EmailNotifier:
    def send(self, message):
        print(f"Email: {message}")


class SmsNotifier:
    def send(self, message):
        print(f"SMS: {message}")


def notify(notifier, message):
    notifier.send(message)


notify(EmailNotifier(), "Заказ создан")
notify(SmsNotifier(), "Заказ создан")
```

Функция `notify()` не знает, какой именно объект ей передали. Ей важно только, что у объекта есть метод `send()`.

## 4. Абстракция

Абстракция означает, что мы выделяем главное поведение и скрываем детали реализации.

Например, приложению может быть важно просто сохранить объект, но не важно, куда именно: в файл, базу данных или память.

```python
class MemoryStorage:
    def __init__(self):
        self.items = []

    def save(self, item):
        self.items.append(item)


class FileStorage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, item):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(str(item) + "\n")
```

Оба класса дают метод `save()`. Остальной код может работать с ними одинаково.

## Абстрактные классы

В Python можно явно описать общий интерфейс через модуль `abc`.

```python
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, item):
        pass


class MemoryStorage(Storage):
    def __init__(self):
        self.items = []

    def save(self, item):
        self.items.append(item)
```

`Storage` говорит: у любого хранилища должен быть метод `save()`.

## Когда использовать наследование

Наследование удобно, когда один класс действительно является частным случаем другого.

Хороший пример:

```python
class Employee:
    pass


class Manager(Employee):
    pass
```

Менеджер — это сотрудник.

Не стоит использовать наследование только для повторного использования кода. Иногда лучше сделать один объект частью другого. Это называется композиция.

```python
class Engine:
    def start(self):
        return "Двигатель запущен"


class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        return self.engine.start()
```

Машина не является двигателем. Машина содержит двигатель.

## Кратко

Инкапсуляция: объект сам контролирует свои данные.

Наследование: один класс может расширять другой.

Полиморфизм: разные объекты можно использовать через одинаковые методы.

Абстракция: код зависит от важного поведения, а не от деталей реализации.
