"""
Этап 03. Репозитории

Цель: вынести SQL-операции в отдельные классы-репозитории
и работать с уже подготовленной PostgreSQL-базой без ORM.

Репозитории создавайте прямо в этом файле.
Модели импортируйте из 01_domain_models/tasks.py.
"""

from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Задание 1
# Импортируйте модели из файла 01_domain_models/tasks.py.
# Не копируйте классы моделей в файл репозиториев.
# Модели не должны знать, что данные хранятся в PostgreSQL.

# TODO: импортировать модели для работы репозиториев
domain_models = import_module("01_domain_models.tasks")
Category = domain_models.Category
Product = domain_models.Product
SizeStock = domain_models.SizeStock
Customer = domain_models.Customer


# Задание 2
# Подключитесь к PostgreSQL через функцию из 02_postgresql_storage/tasks.py.
# Репозитории должны получать готовое соединение через __init__.

# TODO: подключить репозитории к готовому соединению
db_module = import_module("02_postgresql_storage.tasks")
get_connection = db_module.get_connection


# Задание 3
# Создайте репозиторий категорий.
# Он должен добавлять категорию, находить ее по идентификатору и возвращать список категорий.

# TODO: добавить PostgreSQL-репозиторий категорий
class CategoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, category):
        pass

    def get_by_id(self, category_id):
        pass

    def get_all(self):
        pass


# Задание 4
# Создайте репозиторий товаров.
# Он должен добавлять товар в таблицу и находить товар по идентификатору.

# TODO: добавить PostgreSQL-репозиторий товаров
class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, product):
        pass

    def get_by_id(self, product_id):
        pass


# Задание 5
# Добавьте операции получения всех товаров, обновления и удаления.
# Продумайте поведение при повторном идентификаторе и при удалении
# несуществующего товара.

# TODO: расширить операции репозитория товаров
    def get_all(self):
        pass

    def update(self, product):
        pass

    def delete(self, product_id):
        pass


# Задание 6
# Создайте репозиторий остатков по размерам.
# Он должен позволять узнать, сколько единиц конкретного размера есть на складе.

# TODO: добавить PostgreSQL-репозиторий остатков по размерам
class StockRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, stock):
        pass

    def get_quantity(self, product_id, size):
        pass

    def update_quantity(self, product_id, size, quantity):
        pass


# Задание 7
# Создайте репозиторий покупателей.
# Его поведение должно быть похоже на репозиторий товаров.

# TODO: добавить PostgreSQL-репозиторий покупателей
class CustomerRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, customer):
        pass

    def get_by_id(self, customer_id):
        pass

    def get_all(self):
        pass


# Задание 8
# Создайте несколько категорий, товаров, остатков и покупателей, сохраните их в PostgreSQL
# и проверьте основные операции через повторное чтение из базы.

# TODO: добавить ручную проверку репозиториев с реальной БД
if __name__ == "__main__":
    conn = get_connection()
    
    # Создаем репозитории
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    cust_repo = CustomerRepository(conn)
    
    # TODO: проверить работу репозиториев
    
    conn.close()