# Тема 16. `classmethod` и `staticmethod`

## Три вида методов

В классе можно встретить три вида методов:

- обычный метод объекта;
- метод класса;
- статический метод.

Они отличаются тем, что получают первым параметром.

## Обычный метод объекта

Обычный метод получает `self`.

`self` — это текущий объект.

```python
class User:
    def __init__(self, name):
        self.name = name

    def get_info(self):
        return f"Пользователь: {self.name}"
```

Такой метод работает с данными конкретного объекта.

## Метод класса

Метод класса создается с помощью `@classmethod`.

Первым параметром он получает `cls`.

`cls` — это сам класс.

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])


data = {"name": "Anna", "email": "anna@example.com"}
user = User.from_dict(data)
```

Метод класса часто используют для альтернативного создания объектов.

## Почему используется `cls`, а не имя класса

Внутри `from_dict` можно было бы написать так:

```python
return User(data["name"], data["email"])
```

Но лучше использовать `cls`:

```python
return cls(data["name"], data["email"])
```

Так метод будет правильно работать и в дочерних классах.

## Еще пример `classmethod`

Можно создать объект из строки.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @classmethod
    def from_string(cls, text):
        title, price = text.split(";")
        return cls(title, int(price))


product = Product.from_string("Book;500")
```

## Статический метод

Статический метод создается с помощью `@staticmethod`.

Он не получает ни `self`, ни `cls`.

```python
class MathHelper:
    @staticmethod
    def is_even(number):
        return number % 2 == 0


print(MathHelper.is_even(10))
```

Такой метод похож на обычную функцию, но логически находится внутри класса.

## Когда использовать `staticmethod`

`staticmethod` подходит, когда функция связана с темой класса, но ей не нужны данные объекта или класса.

Например, проверка email:

```python
class User:
    def __init__(self, email):
        if not self.is_valid_email(email):
            raise ValueError("Некорректный email")

        self.email = email

    @staticmethod
    def is_valid_email(email):
        return "@" in email
```

Метод `is_valid_email` не использует ни `self`, ни `cls`.

## Сравнение

Обычный метод:

```python
def method(self):
    pass
```

Работает с конкретным объектом.

Метод класса:

```python
@classmethod
def method(cls):
    pass
```

Работает с классом. Часто создает объект.

Статический метод:

```python
@staticmethod
def method():
    pass
```

Не получает объект или класс. Просто логически относится к классу.

## Кратко

`self` — текущий объект.

`cls` — текущий класс.

`@classmethod` удобен для альтернативных конструкторов.

`@staticmethod` удобен для вспомогательных функций внутри класса.
