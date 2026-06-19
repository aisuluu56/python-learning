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
        sql = "INSERT INTO categories (name, description) VALUES (%s, %s) RETURNING id"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (category.name, category.description))
            self.conn.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, category_id):
        sql = "SELECT id, name, description FROM categories WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (category_id,))
            row = cursor.fetchone()
            return Category(row[0], row[1], row[2]) if row else None

    def get_all(self):
        sql = "SELECT id, name, description FROM categories"
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return [Category(row[0], row[1], row[2]) for row in cursor.fetchall()]


# Задание 4
# Создайте репозиторий товаров.
# Он должен добавлять товар в таблицу и находить товар по идентификатору.

# TODO: добавить PostgreSQL-репозиторий товаров
class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, product):
        sql = "INSERT INTO products (category_id, name, price, color, description, is_active) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (product.category.category_id, product.name, product.price, product.color, product.description, product.is_active))
            self.conn.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, product_id):
        sql = "SELECT id, category_id, name, price, color, description, is_active FROM products WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()
            if row:
                cat = Category(row[1], "", "")
                return Product(row[0], row[2], cat, float(row[3]), row[4], row[5] or "", row[6])
            return None


# Задание 5
# Добавьте операции получения всех товаров, обновления и удаления.
# Продумайте поведение при повторном идентификаторе и при удалении
# несуществующего товара.

# TODO: расширить операции репозитория товаров
    def get_all(self):
        sql = "SELECT id, category_id, name, price, color, description, is_active FROM products"
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            products = []
            for row in cursor.fetchall():
                cat = Category(row[1], "", "")
                products.append(Product(row[0], row[2], cat, float(row[3]), row[4], row[5] or "", row[6]))
            return products

    def update(self, product):
        sql = "UPDATE products SET category_id=%s, name=%s, price=%s, color=%s, description=%s, is_active=%s WHERE id=%s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (product.category.category_id, product.name, product.price, product.color, product.description, product.is_active, product.product_id))
            self.conn.commit()
            return cursor.rowcount > 0

    def delete(self, product_id):
        sql = "DELETE FROM products WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (product_id,))
            self.conn.commit()
            return cursor.rowcount > 0


# Задание 6
# Создайте репозиторий остатков по размерам.
# Он должен позволять узнать, сколько единиц конкретного размера есть на складе.

# TODO: добавить PostgreSQL-репозиторий остатков по размерам
class StockRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, stock):
        sql = "INSERT INTO product_stocks (product_id, size, quantity) VALUES (%s,%s,%s)"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (stock.product.product_id, stock.size, stock.quantity))
            self.conn.commit()

    def get_quantity(self, product_id, size):
        sql = "SELECT quantity FROM product_stocks WHERE product_id = %s AND size = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (product_id, size))
            row = cursor.fetchone()
            return row[0] if row else 0

    def update_quantity(self, product_id, size, quantity):
        sql = "UPDATE product_stocks SET quantity = %s WHERE product_id = %s AND size = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (quantity, product_id, size))
            self.conn.commit()


# Задание 7
# Создайте репозиторий покупателей.
# Его поведение должно быть похоже на репозиторий товаров.

# TODO: добавить PostgreSQL-репозиторий покупателей
class CustomerRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, customer):
        sql = "INSERT INTO customers (full_name, phone, email) VALUES (%s,%s,%s) RETURNING id"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (customer.full_name, customer.phone, customer.email))
            self.conn.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, customer_id):
        sql = "SELECT id, full_name, phone, email FROM customers WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (customer_id,))
            row = cursor.fetchone()
            return Customer(row[0], row[1], row[2], row[3]) if row else None

    def get_all(self):
        sql = "SELECT id, full_name, phone, email FROM customers"
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return [Customer(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]


# Задание 8
# Создайте несколько категорий, товаров, остатков и покупателей, сохраните их в PostgreSQL
# и проверьте основные операции через повторное чтение из базы.

# TODO: добавить ручную проверку репозиториев с реальной БД
if __name__ == "__main__":
    conn = get_connection()
    
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    cust_repo = CustomerRepository(conn)
    
    cat = Category(None, "Футболки", "Мужские и женские")
    cat_id = cat_repo.add(cat)
    print(f"Категория создана: {cat_id}")
    
    conn.close()