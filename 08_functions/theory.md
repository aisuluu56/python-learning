# Тема 8. Функции

## Что такое функция

Функция — это именованный блок кода, который можно вызывать несколько раз.

```python
def say_hello():
    print("Hello")

say_hello()
```

## Параметры

Функция может принимать данные.

```python
def greet(name):
    print(f"Привет, {name}!")

greet("Anna")
greet("Ivan")
```

## Возврат результата

`return` возвращает результат из функции.

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)
```

Если функция считает значение, чаще лучше использовать `return`, а не сразу `print()`.

## Значения по умолчанию

```python
def greet(name="student"):
    print(f"Hello, {name}")

greet()
greet("Anna")
```

## Локальные переменные

Переменные, созданные внутри функции, обычно доступны только внутри нее.

```python
def calculate():
    x = 10
    return x * 2

print(calculate())
```

## Функция и цикл

Функции удобно использовать вместе с циклами.

```python
def is_even(number):
    return number % 2 == 0

for n in range(1, 6):
    if is_even(n):
        print(n)
```

## Частые ошибки

Забыли вызвать функцию:

```python
def hello():
    print("Hello")

hello  # ничего не произойдет
```

Правильно:

```python
hello()
```

Забыли `return`:

```python
def add(a, b):
    a + b

result = add(2, 3)
print(result)  # None
```

Правильно:

```python
def add(a, b):
    return a + b
```
