"""
Тема 6. Списки
"""


# Задание 1
# Создайте список из пяти любимых продуктов.
# Выведите первый, третий и последний элемент.

# TODO: решение
products = ["яйца", "капусита", "молоко", "печенье", "орешки"]
print(products[0]) 
print(products[2]) 
print(products[4]) 

# Задание 2
# Создайте список чисел [3, 7, 1, 9, 4].
# Выведите сумму, минимальное и максимальное число.

# TODO: решение
numbers = [3, 7, 1, 9, 4]
print("Сумма:", sum(numbers))
print("Минимум:", min(numbers))
print("Максимум:", max(numbers))


# Задание 3
# Создайте пустой список.
# Спросите у пользователя три имени и добавьте их в список.
# Выведите итоговый список.

# TODO: решение
names = []

name1 = input("Введите первое имя: ")
name2 = input("Введите второе имя: ")
name3 = input("Введите третье имя: ")

names.append(name1)
names.append(name2)
names.append(name3)

print("Список имён:", names)

# Задание 4
# Дан список numbers = [1, 2, 3, 4, 5, 6, 7, 8].
# Создайте новый список только из четных чисел.

# TODO: решение
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)

print("Чётные числа:", even_numbers)

# Задание 5
# Дан список grades = [5, 4, 3, 5, 2, 4, 5].
# Посчитайте среднюю оценку.

# TODO: решение
grades = [5, 4, 3, 5, 2, 4, 5]
average = sum(grades) / len(grades)
print("Средняя оценка:", round(average, 2))

# Задание 6
# Спросите у пользователя пять чисел.
# Добавьте их в список.
# Выведите список в отсортированном виде.

# TODO: решение
numbers = []

print("Введите 5 чисел:")

for i in range(5):
    while True:
        try:
            num = input(f"Число {i+1}: ")
            numbers.append(int(num))
            break
        except ValueError:
            print("❌ Это не число! Попробуй ещё раз.")

numbers.sort()
print("Отсортированный список:", numbers)