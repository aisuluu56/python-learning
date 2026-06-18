# Тема 9. Основы ООП: классы и объекты

## Что такое ООП

ООП — объектно-ориентированное программирование. В этом подходе программа состоит из объектов.

Объект объединяет данные и действия над этими данными.

Например, студент может иметь:

- данные: имя, возраст, группа;
- действия: поздороваться, изменить группу, показать информацию.

## Класс и объект

Класс — это шаблон.

Объект — конкретный экземпляр класса.

```python
class Student:
    pass

student = Student()
```

`Student` — класс, `student` — объект.

## Метод `__init__`

`__init__` вызывается при создании объекта. Обычно в нем задают начальные атрибуты.

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Anna", 18)
```

## `self`

`self` — ссылка на текущий объект.

Через `self` объект хранит свои данные:

```python
self.name = name
```

И вызывает свои методы:

```python
self.say_hello()
```

## Атрибуты

Атрибуты — это переменные внутри объекта.

```python
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

product = Product("Book", 500)
print(product.title)
print(product.price)
```

## Методы

Методы — это функции внутри класса.

```python
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Привет, меня зовут {self.name}")

student = Student("Anna")
student.greet()
```

## Возврат строки из метода

Метод может не печатать результат, а возвращать его.

```python
class Student:
    def __init__(self, name, group):
        self.name = name
        self.group = group

    def get_info(self):
        return f"{self.name}, группа {self.group}"

student = Student("Ivan", "A1")
print(student.get_info())
```

Такой подход удобнее, потому что результат можно использовать в разных местах программы.

## Частые ошибки

Забыли `self` в методе:

```python
class Student:
    def greet():
        print("Hello")
```

Правильно:

```python
class Student:
    def greet(self):
        print("Hello")
```

Забыли обратиться к атрибуту через `self`:

```python
class Student:
    def __init__(self, name):
        name = name
```

Правильно:

```python
class Student:
    def __init__(self, name):
        self.name = name
```
