"""
Тема 8. Функции
"""


# Задание 1
# Напишите функцию greet(name), которая выводит:
# Привет, <name>!
# Вызовите функцию три раза с разными именами.

# TODO: решение
def greet(name):
    print(f"Привет, {name}!")


greet("Алексей")
greet("Мария")
greet("Дмитрий")


# Задание 2
# Напишите функцию add(a, b), которая возвращает сумму двух чисел.
# Вызовите функцию и выведите результат.

# TODO: решение
def add(a, b):
    return a + b


result = add(15, 27)
print("Результат:", result)


# Задание 3
# Напишите функцию is_even(number), которая возвращает True,
# если число чётное, и False, если нечётное.
# Проверьте функцию на нескольких числах.

# TODO: решение
def is_even(number):
    return number % 2 == 0


print(is_even(8))  # True
print(is_even(13))  # False
print(is_even(0))  # True


# Задание 4
# Напишите функцию get_max(a, b, c), которая возвращает наибольшее
# из трех чисел.

# TODO: решение
def get_max(a, b, c):
    return max(a, b, c)


print("Максимум:", get_max(45, 12, 78))


# Задание 5
# Напишите функцию count_vowels(text), которая считает количество
# гласных букв в строке.
# Можно считать гласными: a, e, i, o, u, y.

# TODO: решение
def count_vowels(text):
    vowels = "aeiouy"
    count = 0
    for char in text.lower():
        if char in vowels:
            count += 1
    return count


print("Гласных:", count_vowels("Hello World"))


# Задание 6
# Напишите функцию calculate_total(price, count, discount=0).
# Функция должна возвращать итоговую стоимость:
# price * count минус скидка в процентах.

# TODO: решение
def calculate_total(price, count, discount=0):
    total = price * count
    discount_amount = total * (discount / 100)
    return total - discount_amount


print("Итог:", calculate_total(100, 3, 10))