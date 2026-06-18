"""
Тема 7. Словари
"""


# Задание 1
# Создайте словарь student с ключами:
# name, age, group.
# Выведите каждое значение отдельно.

# TODO: решение
student = {
"name": "Алексей",
"age": 17,
"group": "10А"
}
print(student["name"])
print(student["age"])
print(student["group"])



# Задание 2
# Создайте словарь product с ключами title, price, count.
# Посчитайте общую стоимость товара: price * count.

# TODO: решение
product = {
"title": "Ноутбук",
"price": 65000,
"count": 3
}
total = product["price"] * product["count"]
print("Общая стоимость:", total)



# Задание 3
# Дан словарь user = {"name": "Ivan", "email": "ivan@example.com"}.
# Добавьте ключ age со значением 20.
# Измените email на другой.
# Выведите итоговый словарь.

# TODO: решение
user = {"name": "Ivan", "email": "ivan@example.com"}
user["age"] = 20
user["email"] = "ivan.new@example.com"
print(user)

# Задание 4
# Дан словарь scores = {"Anna": 5, "Ivan": 4, "Maria": 5, "Petr": 3}.
# Выведите имена студентов, у которых оценка 5.

# TODO: решение
scores = {
"Анна": 5,
"Иван": 4,
"Мария": 5,
"Петр": 3
}
print("Отличники:")
for name, grade in scores.items():
    if grade == 5:
        print(name)

# Задание 5
# Спросите у пользователя название страны.
# Есть словарь capitals:
# Russia -> Moscow
# France -> Paris
# Germany -> Berlin
# Если страна есть в словаре, выведите столицу.
# Если нет, выведите "Страна не найдена".

# TODO: решение
capitals = {
"Russia": "Moscow",
"France": "Paris",
"Germany": "Berlin"
}

country = input("Введите название страны (на английском): ")
if country in capitals:
    print(f"Столица {country} — {capitals[country]}")
else:
    print("Страна не найдена в словаре.")


# Задание 6
# Дан текст text = "apple banana apple orange banana apple".
# Посчитайте, сколько раз встречается каждое слово.
# Результат должен быть словарем.

# TODO: решение
text = "apple banana apple orange banana apple"
words = text.split()

word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(word_count)