"""
Этап 03. События и состояние

Цель: добавить обработчики действий пользователя, переменные интерфейса
и обновление окна после событий.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Задание 1
# Создайте окно с полем поиска, выпадающим списком категории и таблицей товаров.
# Можно использовать код из предыдущего этапа.


# TODO: подготовить экран с тестовыми товарами
class StoreApp:
    def __init__(self):
        # Задание 1: Создайте главное окно и разделите его на несколько областей через Frame
        self.root = tk.Tk()
        self.root.title("Магазин одежды 'Айсулуу'")
        self.root.geometry("800x500")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        
        self.top_frame = ttk.Frame(self.root, padding=10)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.top_frame.columnconfigure(1, weight=1)
        
        self.main_frame = ttk.Frame(self.root, padding=5)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        self.bottom_frame = ttk.Frame(self.root, padding=10)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)

# Задание 2
# Создайте StringVar для поисковой строки и выбранной категории.
# Свяжите их с Entry и Combobox.


# TODO: добавить переменные интерфейса
        self.search_var = tk.StringVar()  
        self.category_var = tk.StringVar(value="Все категории")  
        ttk.Label(self.top_frame, text="Поиск:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(self.top_frame, width=30, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.search_btn = ttk.Button(self.top_frame, text="Найти", command=self.search_products)
        self.search_btn.grid(row=0, column=2, padx=5)
        categories = ["Все категории", "Одежда", "Обувь", "Аксессуары"]
        self.category_combo = ttk.Combobox(
            self.top_frame,
            values=categories,
            state="readonly",
            width=15,
            textvariable=self.category_var
        )
        self.category_combo.set("Все категории")
        self.category_combo.grid(row=0, column=3, padx=5)

# Задание 3
# Добавьте обработчик кнопки "Найти".
# Он должен читать текст поиска и обновлять таблицу тестовых товаров.


# TODO: добавить поиск по тестовым данным
        columns = ("id", "name", "category", "price", "color", "status")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена (₽)")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("status", text="Статус")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("category", width=120)
        self.tree.column("price", width=100, anchor="center")
        self.tree.column("color", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.test_products = [
            (1, "Футболка Classic", "Одежда", 1500, "Белый", "В наличии"),
            (2, "Джинсы Slim", "Одежда", 3500, "Синий", "В наличии"),
            (3, "Кроссовки Air", "Обувь", 4500, "Черный", "В наличии"),
            (4, "Сумка кожаная", "Аксессуары", 2800, "Коричневый", "Нет в наличии"),
            (5, "Пальто зимнее", "Одежда", 8900, "Серый", "В наличии"),
            (6, "Ботинки высокие", "Обувь", 5500, "Бежевый", "В наличии"),
            (7, "Шапка вязаная", "Аксессуары", 800, "Красный", "В наличии")
        ]
        self.load_products(self.test_products)

# Задание 4
# Добавьте обработчик выбора строки в Treeview.
# Сохраняйте выбранный товар в атрибуте приложения.


# TODO: сохранить выбранный товар
        self.tree.bind("<<TreeviewSelect>>", self.on_product_selected)
        self.selected_product = None

# Задание 5
# Добавьте кнопку "Добавить в корзину".
# Если товар не выбран, покажите ошибку через messagebox.
# Если выбран, покажите информационное сообщение.


# TODO: добавить обработчик кнопки добавления
        self.add_to_cart_btn = ttk.Button(
            self.bottom_frame,
            text="Добавить в корзину",
            command=self.add_to_cart
        )
        self.add_to_cart_btn.grid(row=0, column=0, padx=5, pady=5)

# Задание 6
# Добавьте строку статуса внизу окна.
# Обновляйте ее после поиска, выбора товара и добавления в корзину.


# TODO: добавить статус приложения


# Задание 7
# Проверьте несколько сценариев:
# пустой поиск, поиск без результатов, выбор строки, клик без выбранного товара.


# TODO: проверить события и сообщения
