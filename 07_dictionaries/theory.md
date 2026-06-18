# Тема 7. Словари

## Что такое словарь

Словарь хранит данные в формате ключ-значение.

```python
student = {
    "name": "Anna",
    "age": 18,
    "group": "A1"
}
```

Ключ — это имя поля. Значение — данные, которые лежат по этому ключу.

## Получение значения

```python
student = {"name": "Anna", "age": 18}

print(student["name"])  # Anna
```

Если ключа может не быть, безопаснее использовать `get()`:

```python
print(student.get("city"))             # None
print(student.get("city", "Unknown"))  # Unknown
```

## Изменение и добавление

```python
student = {"name": "Anna", "age": 18}

student["age"] = 19
student["city"] = "Moscow"

print(student)
```

## Удаление

```python
student = {"name": "Anna", "age": 18}

del student["age"]
print(student)
```

## Перебор словаря

Ключи:

```python
for key in student:
    print(key)
```

Значения:

```python
for value in student.values():
    print(value)
```

Ключи и значения:

```python
for key, value in student.items():
    print(key, value)
```

## Проверка наличия ключа

```python
if "name" in student:
    print("Имя есть")
```

## Частые ошибки

Обращение к несуществующему ключу вызывает ошибку:

```python
student = {"name": "Anna"}
print(student["age"])  # ошибка
```

Используйте `get()`, если ключ может отсутствовать.
