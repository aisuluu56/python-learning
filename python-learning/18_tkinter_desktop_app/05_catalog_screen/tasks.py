"""
Этап 05. Экран каталога
"""
import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import sys
import os

# Путь к корню проекта (поднимаемся на 3 уровня вверх)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Импорт из задания 17
domain = importlib.import_module("17_clothing_store_project.01_domain_models.tasks")
repos = importlib.import_module("17_clothing_store_project.03_repositories.tasks")
catalog_mod = importlib.import_module("17_clothing_store_project.04_catalog_service.tasks")
cart_mod = importlib.import_module("17_clothing_store_project.05_cart.tasks")
db = importlib.import_module("17_clothing_store_project.02_postgresql_storage.tasks")

CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
StockRepository = repos.StockRepository
CatalogService = catalog_mod.CatalogService
CartService = cart_mod.CartService
get_connection = db.get_connection


# ЗАДАНИЕ 1: СОЗДАТЬ ЭКРАН КАТАЛОГА
# TODO: создать экран каталога

class CatalogFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services          # словарь с catalog, cart_service и репозиториями
        self.selected_product_id = None
        self.row_to_product_id = {}

        # ЗАДАНИЕ 4: ПОИСК И ФИЛЬТРЫ
        self._build_search_panel()
        # ЗАДАНИЕ 2: ТАБЛИЦА И ДЕТАЛИ
        self._build_table_and_details()
        # ЗАДАНИЕ 6: РАЗМЕР И КОЛИЧЕСТВО
        self._build_bottom_panel()
        # ЗАДАНИЕ 3: ОБНОВЛЕНИЕ ТАБЛИЦЫ
        self.refresh_products()

    # ЗАДАНИЕ 4: ПОИСК И ФИЛЬТРЫ
    # TODO: добавить поиск и фильтры каталога
    def _build_search_panel(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Поиск:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.search_var, width=15).pack(side="left", padx=5)

        ttk.Label(top, text="Категория:").pack(side="left", padx=5)
        self.cat_var = tk.StringVar(value="Все")
        cats = ["Все"] + [c.name for c in self.services["category_repo"].get_all()]
        ttk.Combobox(top, textvariable=self.cat_var, values=cats, state="readonly", width=10).pack(side="left", padx=5)

        ttk.Label(top, text="Цвет:").pack(side="left", padx=5)
        self.color_var = tk.StringVar(value="Все")
        ttk.Combobox(top, textvariable=self.color_var,
                     values=["Все","Белый","Черный","Синий","Красный"], state="readonly", width=8).pack(side="left", padx=5)

        ttk.Label(top, text="Размер:").pack(side="left", padx=5)
        self.size_var = tk.StringVar(value="Все")
        ttk.Combobox(top, textvariable=self.size_var,
                     values=["Все","S","M","L","XL"], state="readonly", width=5).pack(side="left", padx=5)

        ttk.Button(top, text="Найти", command=self.refresh_products).pack(side="left", padx=5)
        ttk.Button(top, text="Сброс", command=self.reset_filters).pack(side="left", padx=5)

    def reset_filters(self):
        self.search_var.set("")
        self.cat_var.set("Все")
        self.color_var.set("Все")
        self.size_var.set("Все")
        self.refresh_products()

    # ЗАДАНИЕ 2: ТАБЛИЦА И ДЕТАЛИ
    # TODO: добавить таблицу каталога
    def _build_table_and_details(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("name", "category", "price", "color", "status")
        self.tree = ttk.Treeview(main, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column("name", width=150)
        self.tree.column("category", width=100)
        self.tree.column("price", width=80, anchor="center")
        self.tree.column("color", width=80, anchor="center")
        self.tree.column("status", width=80, anchor="center")
        scroll = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # ЗАДАНИЕ 5: ДЕТАЛИ ТОВАРА
        # TODO: добавить детали выбранного товара
        details = ttk.LabelFrame(main, text="Детали", padding=10)
        details.pack(side="right", fill="both", padx=10, expand=True)
        self.detail_text = tk.StringVar(value="Выберите товар")
        ttk.Label(details, textvariable=self.detail_text).pack()
        self.tree.bind("<<TreeviewSelect>>", self.on_product_selected)

    # ЗАДАНИЕ 3: ОБНОВЛЕНИЕ ТАБЛИЦЫ
    # TODO: добавить обновление таблицы товаров
    def refresh_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.row_to_product_id.clear()

        catalog = self.services["catalog"]
        products = catalog.get_active_products()

        # Применяем фильтры
        if (s := self.search_var.get().strip()):
            products = catalog.search_by_name(s)

        cat_name = self.cat_var.get()
        if cat_name != "Все":
            cid = next((c.category_id for c in self.services["category_repo"].get_all() if c.name == cat_name), None)
            if cid is not None:
                products = catalog.filter_by_category(cid)

        color = self.color_var.get()
        if color != "Все":
            products = catalog.filter_by_color(color)

        size = self.size_var.get()
        if size != "Все":
            products = catalog.filter_by_size(size)  # используем сервис

        stock = self.services["stock_repo"]
        for p in products:
            has_stock = any(stock.get_quantity(p.product_id, sz) > 0 for sz in ["S","M","L","XL"])
            status = "В наличии" if has_stock else "Нет"
            row = self.tree.insert("", "end", values=(p.name, p.category.name, p.price, p.color, status))
            self.row_to_product_id[row] = p.product_id

        self.show_status(f"Найдено: {len(products)}")

    # ЗАДАНИЕ 5: ВЫБОР СТРОКИ -> ДЕТАЛИ
    # TODO: добавить детали выбранного товара
    def on_product_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            self.selected_product_id = None
            self.detail_text.set("Выберите товар")
            return
        row = sel[0]
        self.selected_product_id = self.row_to_product_id[row]
        v = self.tree.item(row, "values")
        self.detail_text.set(
            f"Название: {v[0]}\n"
            f"Категория: {v[1]}\n"
            f"Цена: {v[2]} ₽\n"
            f"Цвет: {v[3]}\n"
            f"Наличие: {v[4]}"
        )
        self.show_status(f"Выбран: {v[0]}")

    # ЗАДАНИЕ 6: РАЗМЕР И КОЛИЧЕСТВО
    # TODO: добавить выбор размера и количества
    def _build_bottom_panel(self):
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=5)

        ttk.Label(bottom, text="Размер:").pack(side="left", padx=5)
        self.chosen_size_var = tk.StringVar()
        self.size_combo = ttk.Combobox(bottom, textvariable=self.chosen_size_var,
                                       values=["S","M","L","XL"], state="readonly", width=5)
        self.size_combo.set("M")
        self.size_combo.pack(side="left", padx=5)

        ttk.Label(bottom, text="Кол-во:").pack(side="left", padx=5)
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(bottom, from_=1, to=10, textvariable=self.qty_var, width=5).pack(side="left", padx=5)

        # ЗАДАНИЕ 7: КНОПКА "ДОБАВИТЬ В КОРЗИНУ"
        ttk.Button(bottom, text="Добавить в корзину", command=self.add_to_cart).pack(side="left", padx=20)

    # ЗАДАНИЕ 7: ДОБАВЛЕНИЕ В КОРЗИНУ С ОБРАБОТКОЙ ОШИБОК
    # TODO: добавить товар в корзину через сервис или объект корзины
    def add_to_cart(self):
        if self.selected_product_id is None:
            self.show_error("Выберите товар")
            return
        size = self.chosen_size_var.get()
        if not size:
            self.show_error("Выберите размер")
            return
        try:
            qty = int(self.qty_var.get())
            if qty < 1:
                raise ValueError
        except ValueError:
            self.show_error("Количество должно быть числом > 0")
            return

        available = self.services["stock_repo"].get_quantity(self.selected_product_id, size)
        if available < qty:
            self.show_error(f"Недостаточно. Доступно: {available}")
            return

        product = self.services["product_repo"].get_by_id(self.selected_product_id)
        if not product:
            self.show_error("Товар не найден")
            return

        try:
            self.services["cart_service"].add_to_cart(product, size, qty)
            messagebox.showinfo("Успешно", "Товар добавлен в корзину!")
            self.show_status("Добавлен в корзину")
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, msg):
        messagebox.showerror("Ошибка", msg)

    def show_status(self, msg):
        if hasattr(self.master, 'status_var'):
            self.master.status_var.set(msg)


# ЗАДАНИЕ 8: ПРОВЕРКА ЭКРАНА КАТАЛОГА
# TODO: проверить экран каталога

if __name__ == "__main__":
    conn = get_connection()
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    catalog = CatalogService(prod_repo, cat_repo, stock_repo)
    cart = CartService(catalog, stock_repo)
    services = {
        "catalog": catalog,
        "cart_service": cart,
        "product_repo": prod_repo,
        "stock_repo": stock_repo,
        "category_repo": cat_repo,
    }

    root = tk.Tk()
    root.title("Тест каталога")
    root.geometry("900x600")
    status_var = tk.StringVar(value="Готов")
    ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w", padding=5).pack(fill="x", padx=10, pady=5)

    frame = CatalogFrame(root, services)
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    root.mainloop()
    conn.close()