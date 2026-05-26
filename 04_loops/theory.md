# Тема 4. Циклы `for` и `while`

## Зачем нужны циклы

Циклы позволяют повторять действия несколько раз.

## Цикл `for`

`for` часто используется, когда заранее известно количество повторений.

```python
for i in range(5):
    print(i)
```

Результат:

```text
0
1
2
3
4
```

`range(5)` создает числа от `0` до `4`.

Можно указать начало и конец:

```python
for i in range(1, 6):
    print(i)
```

Можно указать шаг:

```python
for i in range(2, 11, 2):
    print(i)
```

## Цикл `while`

`while` работает, пока условие истинно.

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

Важно менять переменную внутри цикла, иначе цикл может стать бесконечным.

## `break`

`break` завершает цикл досрочно.

```python
while True:
    command = input("Введите команду: ")

    if command == "exit":
        break
```

## `continue`

`continue` пропускает текущую итерацию и переходит к следующей.

```python
for number in range(1, 6):
    if number == 3:
        continue
    print(number)
```

## Накопление результата

Часто в цикле нужно постепенно считать сумму или количество.

```python
total = 0

for number in range(1, 6):
    total += number

print(total)
```

## Частые ошибки

Бесконечный цикл:

```python
count = 1

while count <= 5:
    print(count)
```

Правильно:

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```
