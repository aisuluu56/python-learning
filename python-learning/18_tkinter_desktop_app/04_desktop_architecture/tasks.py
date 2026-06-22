"""
Этап 04. Архитектура desktop-приложения

Цель: отделить GUI-код от backend-логики и подготовить основу приложения,
которое сможет использовать код из задания 17.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# ЗАДАНИЕ 1
# TODO: создать класс DesktopApp

class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Магазин одежды")
        self.root.geometry("600x400")
        self.services = None
    
    def run(self):
        self.root.mainloop()


# ЗАДАНИЕ 2
# TODO: создать классы экранов

class CatalogFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services
        ttk.Label(self, text="Каталог", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Перейти в корзину").pack(pady=5)
        ttk.Button(self, text="Оформить заказ").pack(pady=5)


class CartFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services
        ttk.Label(self, text="Корзина", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Назад в каталог").pack(pady=5)
        ttk.Button(self, text="Оформить заказ").pack(pady=5)


class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services
        ttk.Label(self, text="Оформление заказа", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Назад в корзину").pack(pady=5)
        ttk.Button(self, text="Назад в каталог").pack(pady=5)


# ЗАДАНИЕ 3
# TODO: добавить переключение между экранами

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


# ЗАДАНИЕ 4
# TODO: подготовить сборку зависимостей

class FakeProductRepository:
    def get_all(self):
        return [
            {"id": 1, "name": "Футболка Classic", "price": 1500},
            {"id": 2, "name": "Джинсы Slim", "price": 3500}
        ]


class FakeCartService:
    def __init__(self):
        self.items = []
    
    def add_item(self, product_id):
        self.items.append({"product_id": product_id})
    
    def get_items(self):
        return self.items


class BackendFactory:
    @staticmethod
    def create():
        return {
            "product_repo": FakeProductRepository(),
            "cart_service": FakeCartService()
        }


# ЗАДАНИЕ 5
# TODO: проверить границы ответственности
# ПРАВИЛЬНО: данные приходят через сервис
# НЕПРАВИЛЬНО: прямой доступ к SQL


# ЗАДАНИЕ 6
# TODO: добавить общий показ ошибок

def show_error(message):
    messagebox.showerror("Ошибка", message)


# ЗАДАНИЕ 7
# TODO: проверить навигацию приложения

if __name__ == "__main__":
    app = DesktopApp()
    
    services = BackendFactory.create()
    app.services = services
    
    screen_manager = ScreenManager(app.root)
    
    catalog = CatalogFrame(app.root, services)
    cart = CartFrame(app.root, services)
    checkout = CheckoutFrame(app.root, services)
    
    screen_manager.add_frame("catalog", catalog)
    screen_manager.add_frame("cart", cart)
    screen_manager.add_frame("checkout", checkout)
    
    screen_manager.show_frame("catalog")
    
    app.run()