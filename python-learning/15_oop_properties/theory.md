# Тема 15. `property` и сеттеры

## Зачем нужен `property`

В ООП часто нужно контролировать изменение атрибутов.

Например, цена товара не должна быть отрицательной.

Один вариант — сделать методы `get_price()` и `set_price()`.

```python
class Product:
    def __init__(self, price):
        self._price = price

    def get_price(self):
        return self._price

    def set_price(self, price):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")

        self._price = price
```

Но в Python часто используют `property`.

## Приватный атрибут по договоренности

Одинарное подчеркивание показывает, что атрибут считается внутренним.

```python
self._price = price
```

Это не строгий запрет, а договоренность между программистами.

## `@property`

`@property` позволяет обращаться к методу как к обычному атрибуту.

По смыслу `property` — это геттер. Геттер — это метод, который отвечает за чтение значения.

В других языках часто пишут так:

```python
product.get_price()
```

В Python с `@property` можно читать значение проще:

```python
product.price
```

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def price(self):
        return self._price


product = Product("Book", 500)
print(product.price)
```

Мы пишем `product.price`, а не `product.price()`.

## Сеттер

Сеттер позволяет контролировать присваивание значения.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")

        self._price = value


product = Product("Book", 500)
product.price = 700
```

Когда выполняется `product.price = 700`, Python вызывает сеттер.

## Почему в `__init__` удобно писать `self.price = price`

В примере выше внутри `__init__` используется:

```python
self.price = price
```

Это значит, что начальное значение тоже пройдет проверку в сеттере.

Если передать отрицательную цену, объект не создастся.

## Только для чтения

Если у свойства есть `@property`, но нет сеттера, значение нельзя изменить обычным присваиванием.

```python
class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


user = User("Anna")
print(user.name)
```

Если попробовать выполнить `user.name = "Ivan"`, Python выдаст ошибку.

## Вычисляемое свойство

`property` может не просто возвращать атрибут, а вычислять значение.

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height


rectangle = Rectangle(10, 5)
print(rectangle.area)
```

`area` выглядит как атрибут, но считается каждый раз заново.

## Кратко

`@property` делает метод похожим на атрибут.

Сеттер позволяет проверять значение при присваивании.

Внутренние данные часто хранят в атрибутах с `_`.

Вычисляемые свойства удобны, когда значение зависит от других атрибутов.
