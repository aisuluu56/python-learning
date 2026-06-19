"""
Этап 02. Компоновка и виджеты

Цель: научиться размещать элементы интерфейса и использовать базовые
ttk-виджеты для будущего desktop-приложения магазина.
"""
import tkinter as tk
from tkinter import ttk

# Задание 1
# Создайте главное окно и разделите его на несколько областей через Frame:
# верхняя панель, основная область, нижняя панель.


# TODO: создать структуру окна через Frame
class StoreApp:
    def __init__(self):
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
# В верхнюю панель добавьте поле поиска Entry и кнопку "Найти".


# TODO: добавить панель поиска
        ttk.Label(self.top_frame, text="Поиск:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(self.top_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.search_btn = ttk.Button(self.top_frame, text="Найти", command=self.search_products)
        self.search_btn.grid(row=0, column=2, padx=5)
        

# Задание 3
# Добавьте Combobox для выбора категории.
# На этом этапе можно использовать тестовый список категорий.


# TODO: добавить выбор категории
        categories = ["Все категории", "Одежда", "Обувь", "Аксессуары"]
        self.category_combo = ttk.Combobox(self.top_frame, values=categories, state="readonly", width=15)
        self.category_combo.set("Все категории")
        self.category_combo.grid(row=0, column=3, padx=5)

# Задание 4
# В основной области создайте Treeview для отображения товаров.
# Добавьте колонки: название, категория, цена, цвет, активность.


# TODO: добавить таблицу товаров
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

# Задание 5
# Заполните таблицу несколькими тестовыми строками без подключения к базе данных.


# TODO: добавить тестовые строки в таблицу
        test_products = [
            (1, "Футболка Classic", "Одежда", 1500, "Белый", "В наличии"),
            (2, "Джинсы Slim", "Одежда", 3500, "Синий", "В наличии"),
            (3, "Кроссовки Air", "Обувь", 4500, "Черный", "В наличии"),
            (4, "Сумка кожаная", "Аксессуары", 2800, "Коричневый", "Нет в наличии"),
            (5, "Пальто зимнее", "Одежда", 8900, "Серый", "В наличии")
        ]
        
        for product in test_products:
            self.tree.insert("", "end", values=product)

# Задание 6
# В нижнюю панель добавьте кнопки "Добавить в корзину" и "Очистить фильтры".


# TODO: добавить нижнюю панель действий
        self.add_to_cart_btn = ttk.Button(self.bottom_frame, text="Добавить в корзину", command=self.add_to_cart)
        self.add_to_cart_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.clear_filters_btn = ttk.Button(self.bottom_frame, text="Очистить фильтры", command=self.clear_filters)
        self.clear_filters_btn.grid(row=0, column=1, padx=5, pady=5)
    
    def search_products(self):
        text = self.search_entry.get()
        if text:
            print(f"Поиск: {text}")
        else:
            print("Введите текст для поиска")
    
    def add_to_cart(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            print(f"Добавлено в корзину: {item['values']}")
        else:
            print("Выберите товар")
    
    def clear_filters(self):
        self.search_entry.delete(0, tk.END)
        self.category_combo.set("Все категории")
        print("Фильтры очищены")

# Задание 7
# Проверьте, что при изменении размера окна таблица растягивается,
# а кнопки и поля остаются читаемыми.


# TODO: проверить поведение окна при изменении размера
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StoreApp()
    app.run()