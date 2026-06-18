# Тема 6. Списки

## Что такое список

Список хранит несколько значений в одной переменной.

```python
numbers = [1, 2, 3, 4]
names = ["Anna", "Ivan", "Maria"]
```

В одном списке могут лежать разные типы, но чаще список делают однотипным.

## Индексы

Индексация начинается с нуля.

```python
names = ["Anna", "Ivan", "Maria"]

print(names[0])   # Anna
print(names[-1])  # Maria
```

## Изменение элемента

```python
numbers = [1, 2, 3]
numbers[0] = 10
print(numbers)  # [10, 2, 3]
```

## Добавление и удаление

```python
items = []

items.append("book")
items.append("pen")
print(items)

items.remove("book")
print(items)
```

`pop()` удаляет элемент по индексу и возвращает его.

```python
numbers = [10, 20, 30]
last = numbers.pop()
print(last)     # 30
print(numbers)  # [10, 20]
```

## Перебор списка

```python
numbers = [1, 2, 3]

for number in numbers:
    print(number)
```

Если нужен индекс:

```python
names = ["Anna", "Ivan", "Maria"]

for index, name in enumerate(names):
    print(index, name)
```

## Срезы

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:4])  # [20, 30, 40]
print(numbers[:3])   # [10, 20, 30]
print(numbers[::2])  # [10, 30, 50]
```

## Полезные функции

```python
numbers = [5, 2, 9, 1]

print(len(numbers))
print(sum(numbers))
print(min(numbers))
print(max(numbers))
print(sorted(numbers))
```

## Частые ошибки

Выход за границы списка:

```python
numbers = [1, 2, 3]
print(numbers[5])  # ошибка
```

Проверяйте длину списка через `len()`.
