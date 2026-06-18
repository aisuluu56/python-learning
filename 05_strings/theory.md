# Тема 5. Строки

## Что такое строка

Строка — это последовательность символов.

```python
text = "Python"
```

Строки можно записывать в одинарных или двойных кавычках.

```python
name = 'Anna'
city = "Moscow"
```

## Индексы

У каждого символа есть номер — индекс. Индексация начинается с нуля.

```python
word = "Python"

print(word[0])  # P
print(word[1])  # y
print(word[-1]) # n
```

## Срезы

Срез позволяет получить часть строки.

```python
word = "Python"

print(word[0:2])  # Py
print(word[2:])   # thon
print(word[:4])   # Pyth
```

## Длина строки

```python
text = "hello"
print(len(text))  # 5
```

## Полезные методы

```python
text = "  Hello, Python!  "

print(text.lower())      # нижний регистр
print(text.upper())      # верхний регистр
print(text.strip())      # убрать пробелы по краям
print(text.replace("Python", "world"))
print(text.startswith("  He"))
print(text.endswith("!  "))
```

## Проверка вхождения

```python
text = "I learn Python"

if "Python" in text:
    print("Слово найдено")
```

## Перебор строки

```python
word = "cat"

for letter in word:
    print(letter)
```

## Частые ошибки

Строки неизменяемы. Нельзя заменить символ по индексу напрямую:

```python
word = "cat"
word[0] = "b"  # ошибка
```

Можно создать новую строку:

```python
word = "cat"
new_word = "b" + word[1:]
print(new_word)  # bat
```
