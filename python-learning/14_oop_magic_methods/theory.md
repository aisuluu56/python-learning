# Тема 14. Магические методы

## Что такое магические методы

Магические методы — это специальные методы с двумя подчеркиваниями в начале и в конце имени.

Например:

```python
__init__
__str__
__repr__
__eq__
```

Они вызываются Python автоматически в определенных ситуациях.

С методом `__init__` вы уже знакомы: он вызывается при создании объекта.

## Метод `__str__`

`__str__` отвечает за строковое представление объекта для пользователя.

Он вызывается, когда мы используем `print()` или `str()`.

```python
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Пользователь: {self.name}"


user = User("Anna")
print(user)
```

Без `__str__` Python вывел бы техническую строку с адресом объекта в памяти.

## Метод `__repr__`

`__repr__` отвечает за представление объекта для разработчика.

Обычно он должен быть более точным, чем `__str__`.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __repr__(self):
        return f"Product(title={self.title!r}, price={self.price!r})"


product = Product("Book", 500)
print(product)
```

Если у класса нет `__str__`, но есть `__repr__`, `print()` использует `__repr__`.

## Метод `__eq__`

`__eq__` определяет, как сравнивать объекты через `==`.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __eq__(self, other):
        return self.title == other.title and self.price == other.price


product1 = Product("Book", 500)
product2 = Product("Book", 500)

print(product1 == product2)
```

Без `__eq__` Python сравнивает не данные внутри объектов, а сами объекты.

## Проверка типа в `__eq__`

В реальном коде полезно проверять, что сравниваемый объект нужного типа.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False

        return self.title == other.title and self.price == other.price
```

Так код не сломается, если сравнить продукт со строкой или числом.

## Метод `__len__`

`__len__` вызывается функцией `len()`.

```python
class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def __len__(self):
        return len(self.tasks)


task_list = TaskList()
task_list.add_task("Купить хлеб")
task_list.add_task("Сделать домашку")

print(len(task_list))
```

## Методы сравнения

Метод `__lt__` определяет поведение оператора `<`.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __lt__(self, other):
        return self.price < other.price


book = Product("Book", 500)
phone = Product("Phone", 30000)

print(book < phone)
```

Это удобно, когда объекты нужно сравнивать или сортировать.

## Кратко

`__str__` нужен для понятного вывода объекта.

`__repr__` нужен для технического представления объекта.

`__eq__` задает сравнение через `==`.

`__len__` позволяет использовать `len()`.

`__lt__` задает сравнение через `<`.
