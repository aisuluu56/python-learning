"""
Этап 08. Итоговое desktop-приложение

Цель: собрать единое tkinter-приложение магазина одежды, которое использует
backend из задания 17 и позволяет пройти путь от каталога до заказа.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import sys
import os

# Путь к корню проекта (поднимаемся на 3 уровня вверх)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ===== Задание 2: подключение backend из задания 17 =====
db = importlib.import_module("17_clothing_store_project.02_postgresql_storage.tasks")
repos = importlib.import_module("17_clothing_store_project.03_repositories.tasks")
catalog_mod = importlib.import_module("17_clothing_store_project.04_catalog_service.tasks")
cart_mod = importlib.import_module("17_clothing_store_project.05_cart.tasks")
order_mod = importlib.import_module("17_clothing_store_project.06_orders.tasks")
discount_mod = importlib.import_module("17_clothing_store_project.07_users_discounts.tasks")

get_connection = db.get_connection
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
StockRepository = repos.StockRepository
CustomerRepository = repos.CustomerRepository
OrderRepository = order_mod.OrderRepository
PromocodeRepository = discount_mod.PromocodeRepository
CatalogService = catalog_mod.CatalogService
CartService = cart_mod.CartService
ExtendedOrderService = discount_mod.ExtendedOrderService
DiscountService = discount_mod.DiscountService

# ===== Импорт экранов из этапов 05-07 =====
# Если экраны в отдельных файлах, раскомментируйте:
# from tasks_05_catalog_screen import CatalogFrame
# from tasks_06_cart_screen import CartFrame
# from tasks_07_checkout_screen import CheckoutFrame

# Временно используем заглушки (замените на реальные импорты)
class CatalogFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        ttk.Label(self, text="Каталог (заглушка)").pack()
    def refresh(self): pass

class CartFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        ttk.Label(self, text="Корзина (заглушка)").pack()
    def refresh(self): pass

class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        ttk.Label(self, text="Оформление (заглушка)").pack()
    def refresh(self): pass


# ===== Задание 3: менеджер экранов =====
# TODO: добавить навигацию

class ScreenManager:
    def __init__(self, root):
        self.root = root
        self.frames = {}

    def add_frame(self, name, frame):
        self.frames[name] = frame
        frame.pack(fill="both", expand=True)
        frame.pack_forget()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)


# ===== Задание 1: финальный класс приложения =====
# TODO: создать финальный класс приложения

class ClothingStoreDesktopApp:
    def __init__(self):
        # Задание 8: улучшение внешнего вида
        self.root = tk.Tk()
        self.root.title("Магазин одежды 'Стиль'")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # Настройка стиля
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("Treeview", rowheight=26)

        # Строка статуса
        self.status_var = tk.StringVar(value="Добро пожаловать!")
        status_label = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=5
        )
        status_label.pack(side="bottom", fill="x", padx=10, pady=5)

        # ===== Сборка зависимостей =====
        self.conn = get_connection()
        self.category_repo = CategoryRepository(self.conn)
        self.product_repo = ProductRepository(self.conn)
        self.stock_repo = StockRepository(self.conn)
        self.customer_repo = CustomerRepository(self.conn)
        self.order_repo = OrderRepository(self.conn)
        self.promo_repo = PromocodeRepository(self.conn)

        self.catalog_service = CatalogService(
            self.product_repo, self.category_repo, self.stock_repo
        )
        self.cart_service = CartService(self.catalog_service, self.stock_repo)
        self.discount_service = DiscountService(self.promo_repo)
        self.order_service = ExtendedOrderService(
            self.stock_repo, self.customer_repo, self.order_repo,
            self.conn, self.discount_service
        )

        self.services = {
            "catalog": self.catalog_service,
            "cart_service": self.cart_service,
            "order_service": self.order_service,
            "discount_service": self.discount_service,
            "stock_repo": self.stock_repo,
            "product_repo": self.product_repo,
            "category_repo": self.category_repo,
            "customer_repo": self.customer_repo,
        }

        # ===== Задание 4: подключение экранов =====
        # TODO: подключить экраны приложения

        self.screen_manager = ScreenManager(self.root)
        self.catalog_frame = CatalogFrame(self.root, self.services)
        self.cart_frame = CartFrame(self.root, self.services)
        self.checkout_frame = CheckoutFrame(self.root, self.services)

        self.screen_manager.add_frame("catalog", self.catalog_frame)
        self.screen_manager.add_frame("cart", self.cart_frame)
        self.screen_manager.add_frame("checkout", self.checkout_frame)

        # Передаём менеджер в экраны для навигации
        for frame in [self.catalog_frame, self.cart_frame, self.checkout_frame]:
            frame.screen_manager = self.screen_manager
            frame.status_var = self.status_var

        self.screen_manager.show_frame("catalog")

    # ===== Задание 5: обновление при переходе =====
    # TODO: добавить обновление экранов при навигации

    def show_frame(self, name):
        frame = self.screen_manager.frames[name]
        if hasattr(frame, "refresh"):
            try:
                frame.refresh()
            except Exception as e:
                self.show_error(str(e))
        self.screen_manager.show_frame(name)

    # ===== Задание 6: общая обработка ошибок =====
    # TODO: добавить обработку ошибок

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)
        self.status_var.set(f"Ошибка: {message}")

    def run(self):
        self.root.mainloop()


# ===== Задание 7-8: проверка полного сценария =====
# TODO: проверить полный сценарий
# TODO: улучшить удобство интерфейса

if __name__ == "__main__":
    app = ClothingStoreDesktopApp()
    app.run()
    app.conn.close()