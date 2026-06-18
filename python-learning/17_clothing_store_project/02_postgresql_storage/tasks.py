"""
Этап 02. PostgreSQL: база, схема и подключение

Цель: подготовить реальную PostgreSQL-базу данных, SQL-схему
и подключение из Python без ORM.

SQL-схему описывайте в файле:
schema.sql

Функцию подключения к БД создавайте прямо в этом файле.
Следующие этапы будут импортировать ее отсюда.
"""

import os
import psycopg2


# Задание 1
# Создайте PostgreSQL-базу данных для проекта.
# Продумайте имя базы, пользователя, пароль и способ хранения параметров подключения.

# TODO: создать базу данных PostgreSQL
# Параметры подключения
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "clothing_store"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


# Задание 2
# Установите драйвер PostgreSQL для Python.
# Выберите один вариант драйвера и используйте его во всем проекте.

# TODO: установить драйвер PostgreSQL
# pip install psycopg2-binary


# Задание 3
# Создайте отдельный файл для подключения к БД.
# Вынесите туда функцию, которая читает параметры подключения
# и возвращает готовое соединение.

# TODO: добавить функцию подключения к БД
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# Задание 4
# Подготовьте SQL-схему первых таблиц:
# категории, товары, остатки товаров по размерам и покупатели.

# TODO: описать первые таблицы в schema.sql
# Создайте файл schema.sql с SQL-запросами


# Задание 5
# Добавьте первичные ключи, внешние ключи и ограничения.
# Связи между таблицами должны быть описаны в SQL, а не внутри моделей.

# TODO: добавить связи и ограничения в SQL-схему
# Добавьте FOREIGN KEY и CHECK в schema.sql


# Задание 6
# Подготовьте способ создания таблиц.
# Это может быть ручной запуск SQL-файла или отдельный Python-файл,
# который выполняет команды из schema.sql.

# TODO: добавить запуск SQL-схемы


# Задание 7
# Проверьте подключение простым SQL-запросом.
# Например, можно выполнить запрос, который возвращает одно значение.

# TODO: проверить соединение с реальной БД
def check_connection():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result[0] == 1
        conn.close()
    except:
        return False


# Задание 8
# Проверьте, что таблицы действительно созданы.
# Для проверки можно выполнить SELECT к одной из таблиц.

# TODO: проверить созданные таблицы
def check_tables():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('categories', 'products', 'product_stocks', 'customers')
        """)
        tables = cursor.fetchall()
        return [t[0] for t in tables]
    conn.close()


if __name__ == "__main__":
    print(check_connection())
    print(check_tables())