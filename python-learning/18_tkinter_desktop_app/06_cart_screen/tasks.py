"""
Этап 06. Экран корзины
"""
import tkinter as tk
from tkinter import ttk, messagebox
import importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Импорт из задания 17
domain = importlib.import_module("17_clothing_store_project.01_domain_models.tasks")
repos = importlib.import_module("17_clothing_store_project.03_repositories.tasks")
catalog_mod = importlib.import_module("17_clothing_store_project.04_catalog_service.tasks")
cart_mod = importlib.import_module("17_clothing_store_project.05_cart.tasks")
db = importlib.import_module("17_clothing_store_project.02_postgresql_storage.tasks")

Category = domain.Category
Product = domain.Product
SizeStock = domain.SizeStock
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
StockRepository = repos.StockRepository
CatalogService = catalog_mod.CatalogService
CartService = cart_mod.CartService
Cart = cart_mod.Cart
CartItem = cart_mod.CartItem
get_connection = db.get_connection


# Задание 1: создать экран корзины
class CartFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services          # словарь с cart_service, stock_repo и др.
        self.selected_idx = None
        self.row_to_idx = {}

        self.create_table()
        self.create_buttons()
        self.refresh_cart()

    # Задание 2: таблица корзины
    def create_table(self):
        cols = ("name", "size", "price", "quantity", "total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("name", width=150)
        self.tree.column("size", width=60, anchor="center")
        self.tree.column("price", width=80, anchor="center")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("total", width=80, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scroll.pack(side="right", fill="y", pady=5)

        # Задание 4: выбор позиции
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        self.total_label = ttk.Label(self, text="Итого: 0 ₽", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=5)

    # Задание 3: обновление корзины
    def refresh_cart(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.row_to_idx.clear()

        cart = self.services["cart_service"].get_cart()
        items = cart.get_items()
        total = 0

        for idx, item in enumerate(items):
            row = self.tree.insert("", "end", values=(
                item.product.name,
                item.size,
                item.price,
                item.quantity,
                item.get_total()
            ))
            self.row_to_idx[row] = idx
            total += item.get_total()

        self.total_label.config(text=f"Итого: {total} ₽")

    # Задание 4: выбор позиции
    def on_item_selected(self, event):
        sel = self.tree.selection()
        self.selected_idx = self.row_to_idx.get(sel[0]) if sel else None

    def get_selected_index(self):
        return self.selected_idx

    def create_buttons(self):
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=5)

        # Задание 5: изменение количества
        ttk.Label(bottom, text="Новое кол-во:").pack(side="left", padx=5)
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(bottom, from_=1, to=10, textvariable=self.qty_var, width=5).pack(side="left", padx=5)
        ttk.Button(bottom, text="Изменить кол-во", command=self.change_quantity).pack(side="left", padx=5)

        # Задание 6: удаление позиции
        ttk.Button(bottom, text="Удалить позицию", command=self.remove_item).pack(side="left", padx=5)

        # Задание 7: очистка корзины
        ttk.Button(bottom, text="Очистить корзину", command=self.clear_cart).pack(side="left", padx=5)

        # Задание 8: оформление заказа
        ttk.Button(bottom, text="Оформить заказ", command=self.checkout).pack(side="right", padx=5)
        ttk.Button(bottom, text="Назад в каталог", command=self.go_back).pack(side="right", padx=5)

    # Задание 5: изменение количества
    def change_quantity(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showerror("Ошибка", "Выберите позицию")
            return

        try:
            new_qty = int(self.qty_var.get())
            if new_qty < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число >0")
            return

        cart = self.services["cart_service"].get_cart()
        items = cart.get_items()
        if idx >= len(items):
            return
        item = items[idx]
        product_id = item.product.product_id
        size = item.size

        # Проверка остатка
        available = self.services["stock_repo"].get_quantity(product_id, size)
        if available < new_qty:
            messagebox.showerror("Ошибка", f"Недостаточно. Доступно: {available}")
            return

        self.services["cart_service"].update_quantity(product_id, size, new_qty)
        self.refresh_cart()

    # Задание 6: удаление позиции
    def remove_item(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showerror("Ошибка", "Выберите позицию")
            return

        cart = self.services["cart_service"].get_cart()
        items = cart.get_items()
        if idx >= len(items):
            return
        item = items[idx]
        self.services["cart_service"].remove_from_cart(item.product.product_id, item.size)
        self.refresh_cart()

    # Задание 7: очистка корзины
    def clear_cart(self):
        cart = self.services["cart_service"].get_cart()
        if not cart.get_items():
            messagebox.showerror("Ошибка", "Корзина уже пуста")
            return

        if messagebox.askyesno("Подтверждение", "Очистить корзину?"):
            self.services["cart_service"].clear_cart()
            self.refresh_cart()

    # Задание 8: переход к оформлению
    def checkout(self):
        cart = self.services["cart_service"].get_cart()
        if not cart.get_items():
            messagebox.showerror("Ошибка", "Корзина пуста")
            return
        if hasattr(self.master, 'screen_manager'):
            self.master.screen_manager.show_frame("checkout")

    def go_back(self):
        if hasattr(self.master, 'screen_manager'):
            self.master.screen_manager.show_frame("catalog")


# ===== ТЕСТОВЫЙ ЗАПУСК (требует работающей БД) =====
if __name__ == "__main__":
    conn = get_connection()
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    catalog = CatalogService(prod_repo, cat_repo, stock_repo)
    cart_service = CartService(catalog, stock_repo)

    # Добавляем тестовые товары (если есть в БД)
    # Здесь нужно, чтобы в БД были товары с id 1 и 3
    try:
        p1 = prod_repo.get_by_id(1)
        p3 = prod_repo.get_by_id(3)
        if p1 and p3:
            cart_service.add_to_cart(p1, "M", 2)
            cart_service.add_to_cart(p3, "L", 1)
    except:
        pass

    services = {
        "cart_service": cart_service,
        "stock_repo": stock_repo,
        "catalog": catalog,
        "product_repo": prod_repo,
    }

    root = tk.Tk()
    root.title("Тест корзины")
    root.geometry("700x450")
    frame = CartFrame(root, services)
    frame.pack(fill="both", expand=True)
    root.mainloop()
    conn.close()