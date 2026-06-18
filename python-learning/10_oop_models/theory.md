# Тема 10. Классы-модели

## Что такое модель

Модель — это класс, который описывает объект предметной области.

Примеры моделей:

- `User` — пользователь;
- `Product` — товар;
- `Order` — заказ;
- `Task` — задача;
- `Book` — книга.

Модель обычно хранит состояние и содержит методы, которые относятся именно к этому объекту.

## Пример модели

```python
class Product:
    def __init__(self, title, price, count):
        self.title = title
        self.price = price
        self.count = count

    def get_total_price(self):
        return self.price * self.count
```

Использование:

```python
product = Product("Book", 500, 3)
print(product.get_total_price())
```

## Состояние объекта

Состояние — это значения атрибутов объекта в текущий момент.

```python
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True
```

До вызова `mark_done()` задача не выполнена. После вызова состояние меняется.

## Валидация

Модель может проверять данные, чтобы объект не создавался в неправильном состоянии.

```python
class Product:
    def __init__(self, title, price):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")

        self.title = title
        self.price = price
```

`raise ValueError(...)` останавливает выполнение и сообщает об ошибке данных.

## Метод `to_dict`

Часто модель нужно превратить в словарь, чтобы сохранить или отправить данные.

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
        }
```

## Метод `from_dict`

Иногда объект нужно создать из словаря.

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])
```

`cls` — ссылка на класс. Через нее можно создать новый объект.

## Почему модели полезны

Без модели данные часто живут в разрозненных словарях:

```python
product = {"title": "Book", "price": 500, "count": 3}
```

С моделью поведение находится рядом с данными:

```python
product = Product("Book", 500, 3)
print(product.get_total_price())
```

Так код легче читать, проверять и расширять.
