# Тема 13. Атрибуты класса и атрибуты объекта

## Атрибуты объекта

Атрибут объекта принадлежит конкретному объекту.

Обычно такие атрибуты создаются внутри `__init__` через `self`.

```python
class Student:
    def __init__(self, name):
        self.name = name


student1 = Student("Anna")
student2 = Student("Ivan")

print(student1.name)
print(student2.name)
```

У каждого объекта свое значение `name`.

## Атрибуты класса

Атрибут класса принадлежит самому классу и является общим для всех объектов.

```python
class Student:
    school_name = "Python School"

    def __init__(self, name):
        self.name = name


student1 = Student("Anna")
student2 = Student("Ivan")

print(student1.school_name)
print(student2.school_name)
```

`school_name` общий для всех студентов.

## Когда использовать атрибуты класса

Атрибуты класса удобно использовать для общих значений:

- название школы;
- налоговая ставка;
- максимальное количество попыток;
- роли или статусы;
- счетчик созданных объектов.

Пример с константой:

```python
class Order:
    STATUS_NEW = "new"
    STATUS_PAID = "paid"

    def __init__(self, number):
        self.number = number
        self.status = self.STATUS_NEW
```

## Счетчик объектов

Атрибут класса может хранить общее состояние для всех объектов.

```python
class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1


user1 = User("Anna")
user2 = User("Ivan")

print(User.count)
```

После создания двух пользователей `User.count` будет равен `2`.

## Обращение через класс и через объект

К атрибуту класса лучше обращаться через имя класса:

```python
print(User.count)
```

Так сразу видно, что значение относится ко всему классу.

Через объект тоже можно:

```python
print(user1.count)
```

Но такой вариант может запутать: кажется, что `count` принадлежит только `user1`.

## Важная особенность

Если записать значение через объект, Python создаст атрибут объекта с таким же именем.

```python
class Product:
    currency = "руб."


book = Product()
phone = Product()

book.currency = "долл."

print(book.currency)
print(phone.currency)
print(Product.currency)
```

У `book` появится свой атрибут `currency`. Атрибут класса при этом не изменится.

## Кратко

Атрибут объекта хранит данные конкретного объекта.

Атрибут класса хранит общее значение для всего класса.

Если значение должно быть разным у разных объектов, используйте `self`.

Если значение общее для всех объектов, используйте атрибут класса.
