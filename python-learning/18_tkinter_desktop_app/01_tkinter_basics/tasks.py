"""
Этап 01. Основы tkinter

Цель: создать первое desktop-окно приложения и познакомиться с базовыми
виджетами tkinter.

На этом этапе не подключайте базу данных и backend из задания 17.
Сначала нужно понять, как работает окно и главный цикл.
"""
import tkinter as tk

# Задание 1
# Импортируйте tkinter и создайте главное окно приложения.
# Задайте заголовок окна и начальный размер.


# TODO: создать главное окно
class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Магазин одежды 'Айсулуу'")
        self.root.geometry("500x400")
        
        self.title_label = tk.Label(
            self.root,
            text="Добро пожаловать в магазин одежды 'Айсулуу'",
            font=("Arial", 14, "bold")
        )
        self.title_label.pack(pady=20)
        
        self.catalog_btn = tk.Button(
            self.root,
            text="Каталог",
            width=20,
            height=2
        )
        self.catalog_btn.pack(pady=5)
        
        self.cart_btn = tk.Button(
            self.root,
            text="Корзина",
            width=20,
            height=2
        )
        self.cart_btn.pack(pady=5)
        
        self.order_btn = tk.Button(
            self.root,
            text="Оформить заказ",
            width=20,
            height=2
        )
        self.order_btn.pack(pady=5)
        
        self.exit_btn = tk.Button(
            self.root,
            text="Выход",
            width=20,
            height=2,
            command=self.close_app
        )
        self.exit_btn.pack(pady=5)
    
    def close_app(self):
        self.root.destroy()

# Задание 2
# Добавьте в окно заголовок приложения через Label.
# Текст должен быть связан с будущим магазином одежды.


# TODO: добавить Label с названием приложения


# Задание 3
# Добавьте несколько кнопок-заглушек:
# "Каталог", "Корзина", "Оформить заказ", "Выход".
# Пока кнопки могут ничего не делать.


# TODO: добавить кнопки главного меню


# Задание 4
# Добавьте обработчик для кнопки "Выход", который закрывает окно.


# TODO: добавить закрытие окна по кнопке


# Задание 5
# Перепишите код в виде класса DesktopApp.
# У класса должен быть метод run(), который запускает mainloop().


# TODO: оформить первое приложение как класс


# Задание 6
# Запустите файл и проверьте, что окно открывается, кнопки видны,
# а кнопка выхода закрывает приложение.


# TODO: добавить ручную проверку запуска
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopApp()
    app.run()