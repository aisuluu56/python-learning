"""
Этап 03. События и состояние

Цель: добавить обработчики действий пользователя, переменные интерфейса
и обновление окна после событий.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StoreApp:
    def __init__(self):
        # Задание 1
        # Создайте окно с полем поиска, выпадающим списком категории и таблицей товаров.
        # Можно использовать код из предыдущего этапа.
        # TODO: подготовить экран с тестовыми товарами
        
        # ТЕОРИЯ: СОЗДАНИЕ ГЛАВНОГО ОКНА
        # Tk() - главное окно приложения
        self.root = tk.Tk()
        self.root.title("Магазин одежды 'Айсулуу'")
        self.root.geometry("800x500")
        
        # ТЕОРИЯ: НАСТРОЙКА РАСТЯГИВАНИЯ (grid)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        
        # ТЕОРИЯ: FRAME - КОНТЕЙНЕР ДЛЯ ВИДЖЕТОВ
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
        
        # ТЕОРИЯ: LABEL - ТЕКСТОВАЯ НАДПИСЬ
        ttk.Label(self.top_frame, text="Поиск:").grid(row=0, column=0, padx=5)
        
        # ТЕОРИЯ: ENTRY - ПОЛЕ ВВОДА
        self.search_entry = ttk.Entry(self.top_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        # ТЕОРИЯ: BUTTON - КНОПКА
        self.search_btn = ttk.Button(self.top_frame, text="Найти")
        self.search_btn.grid(row=0, column=2, padx=5)
        
        # ТЕОРИЯ: COMBOBOX - ВЫПАДАЮЩИЙ СПИСОК
        categories = ["Все категории", "Одежда", "Обувь", "Аксессуары"]
        self.category_combo = ttk.Combobox(
            self.top_frame,
            values=categories,
            state="readonly",
            width=15
        )
        self.category_combo.set("Все категории")
        self.category_combo.grid(row=0, column=3, padx=5)
        
        # ТЕОРИЯ: TREEVIEW - ТАБЛИЦА
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
        
        # ТЕОРИЯ: SCROLLBAR - ПОЛОСА ПРОКРУТКИ
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # ТЕОРИЯ: ТЕСТОВЫЕ ДАННЫЕ
        self.test_products = [
            (1, "Футболка Classic", "Одежда", 1500, "Белый", "В наличии"),
            (2, "Джинсы Slim", "Одежда", 3500, "Синий", "В наличии"),
            (3, "Кроссовки Air", "Обувь", 4500, "Черный", "В наличии"),
            (4, "Сумка кожаная", "Аксессуары", 2800, "Коричневый", "Нет в наличии"),
            (5, "Пальто зимнее", "Одежда", 8900, "Серый", "В наличии"),
            (6, "Ботинки высокие", "Обувь", 5500, "Бежевый", "В наличии"),
            (7, "Шапка вязаная", "Аксессуары", 800, "Красный", "В наличии")
        ]
        
        for product in self.test_products:
            self.tree.insert("", "end", values=product)
        
        # Задание 2
        # Создайте StringVar для поисковой строки и выбранной категории.
        # Свяжите их с Entry и Combobox.
        # TODO: добавить переменные интерфейса
        
        # ТЕОРИЯ: ПЕРЕМЕННЫЕ ИНТЕРФЕЙСА (StringVar)
        # StringVar - специальная переменная для хранения строки
        # .get() - получить значение
        # .set() - установить значение
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Все категории")
        self.search_entry.config(textvariable=self.search_var)
        self.category_combo.config(textvariable=self.category_var)
        
        # Задание 3
        # Добавьте обработчик кнопки "Найти".
        # Он должен читать текст поиска и обновлять таблицу тестовых товаров.
        # TODO: добавить поиск по тестовым данным
        
        # ТЕОРИЯ: BUTTON - command (обработчик события нажатия)
        self.search_btn.config(command=self.search_products)
        
        # Задание 4
        # Добавьте обработчик выбора строки в Treeview.
        # Сохраняйте выбранный товар в атрибуте приложения.
        # TODO: сохранить выбранный товар
        
        # ТЕОРИЯ: BIND - ПРИВЯЗКА СОБЫТИЙ
        # bind(событие, функция-обработчик)
        # <<TreeviewSelect>> - событие выбора строки в таблице
        self.tree.bind("<<TreeviewSelect>>", self.on_product_selected)
        
        # ТЕОРИЯ: СОСТОЯНИЕ ПРИЛОЖЕНИЯ
        self.selected_product = None
        
        # Задание 5
        # Добавьте кнопку "Добавить в корзину".
        # Если товар не выбран, покажите ошибку через messagebox.
        # Если выбран, покажите информационное сообщение.
        # TODO: добавить обработчик кнопки добавления
        
        # ТЕОРИЯ: КНОПКА "Добавить в корзину"
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
        
        # ТЕОРИЯ: СТРОКА СТАТУСА
        self.status_var = tk.StringVar(value="Готов к работе")
        self.status_label = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=5
        )
        self.status_label.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
    
    # ТЕОРИЯ: ОБНОВЛЕНИЕ ТАБЛИЦЫ
    def load_products(self, products):
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)
        for product in products:
            self.tree.insert("", "end", values=product)
    
    # Задание 3
    # TODO: добавить поиск по тестовым данным
    
    # ТЕОРИЯ: ОБРАБОТЧИК СОБЫТИЯ - ПОИСК
    def search_products(self):
        search_text = self.search_var.get().lower()
        selected_category = self.category_var.get()
        
        found = []
        for product in self.test_products:
            name_match = search_text in product[1].lower() if search_text else True
            category_match = (selected_category == "Все категории" or 
                            product[2] == selected_category)
            if name_match and category_match:
                found.append(product)
        
        self.load_products(found)
        
        if found:
            self.status_var.set(f"Найдено: {len(found)} товаров")
        else:
            self.status_var.set("Ничего не найдено")
    
    # Задание 4
    # TODO: сохранить выбранный товар
    
    # ТЕОРИЯ: ОБРАБОТЧИК СОБЫТИЯ - ВЫБОР СТРОКИ
    def on_product_selected(self, event):
        selected_rows = self.tree.selection()
        if not selected_rows:
            self.selected_product = None
            self.status_var.set("Товар не выбран")
            return
        
        selected_row = selected_rows[0]
        values = self.tree.item(selected_row, "values")
        self.selected_product = {
            "id": values[0],
            "name": values[1],
            "category": values[2],
            "price": values[3],
            "color": values[4],
            "status": values[5]
        }
        self.status_var.set(f"Выбран товар: {values[1]}")
    
    # Задание 5
    # TODO: добавить обработчик кнопки добавления
    
    # ТЕОРИЯ: ОБРАБОТЧИК СОБЫТИЯ - ДОБАВЛЕНИЕ В КОРЗИНУ
    # messagebox.showerror() - сообщение об ошибке
    # messagebox.showinfo() - информационное сообщение
    def add_to_cart(self):
        if self.selected_product is None:
            messagebox.showerror("Ошибка", "Сначала выберите товар в таблице!")
            self.status_var.set("Ошибка: товар не выбран")
            return
        
        product_name = self.selected_product["name"]
        messagebox.showinfo("Успешно!", f"Товар '{product_name}' добавлен в корзину!")
        self.status_var.set(f"Добавлен в корзину: {product_name}")
    
    # Задание 7
    # Проверьте несколько сценариев:
    # пустой поиск, поиск без результатов, выбор строки, клик без выбранного товара.
    # TODO: проверить события и сообщения
    
    # ТЕОРИЯ: ЗАПУСК ПРИЛОЖЕНИЯ
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StoreApp()
    app.run()