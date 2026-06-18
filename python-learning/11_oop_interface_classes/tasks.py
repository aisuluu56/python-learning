"""
Тема 11. Классы для интерфейса
"""


# Задание 1
# Создайте модель User с атрибутом name.
# Добавьте метод get_greeting(), который возвращает приветствие.
# Важно: внутри User нельзя использовать input() и print().

# TODO: решение
class User:
    def __init__(self, name):
        self.name = name

    def get_greeting(self):
        return f"Привет, {self.name}!"


# Задание 2
# Создайте класс ConsoleUserInterface.
# Добавьте метод ask_name(), который спрашивает имя через input().
# Добавьте метод show_message(message), который выводит сообщение через print().

# TODO: решение
class ConsoleUserInterface:
    def ask_name(self):
        return input("Введите ваше имя: ")

    def show_message(self, message):
        print(message)


# Задание 3
# Создайте класс App.
# В __init__ он должен принимать interface.
# В методе run() он должен:
# 1. спросить имя через interface;
# 2. создать User;
# 3. показать приветствие через interface.

# TODO: решение
class App:
    def __init__(self, interface):
        self.interface = interface

    def run(self):
        name = self.interface.ask_name()
        user = User(name)
        self.interface.show_message(user.get_greeting())


# Задание 4
# Создайте модель Task.
# Атрибуты: title, is_done.
# Добавьте метод mark_done().
# Создайте интерфейс ConsoleTaskInterface с методами:
# ask_task_title(), show_task(task).

# TODO: решение
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True


class ConsoleTaskInterface:
    def ask_task_title(self):
        return input("Название задачи: ")

    def show_task(self, task):
        status = "✓ выполнено" if task.is_done else "✗ не выполнено"
        print(f"  {task.title}: {status}")


# Задание 5
# Создайте класс TaskApp.
# Он должен хранить список задач.
# Через интерфейс он должен уметь добавить задачу и показать все задачи.
# Пока можно без бесконечного меню: просто вызовите методы вручную.

# TODO: решение
class TaskApp:
    def __init__(self, interface):
        self.interface = interface
        self.tasks = []

    def add_task(self):
        title = self.interface.ask_task_title()
        task = Task(title)
        self.tasks.append(task)
        self.interface.show_message(f"Задача '{title}' добавлена!")

    def show_all_tasks(self):
        if not self.tasks:
            self.interface.show_message("Список задач пуст.")
            return
        
        self.interface.show_message("\nСписок задач:")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. ", end="")
            self.interface.show_task(task)

    def mark_task_done(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_done()
            self.interface.show_message("Задача отмечена как выполненная!")
        else:
            self.interface.show_message("Неверный номер задачи!")


# Задание 6
# Создайте класс Menu.
# Метод show() выводит пункты:
# 1. Добавить задачу
# 2. Показать задачи
# 0. Выход
# Метод ask_choice() возвращает выбор пользователя.
# Подумайте, как этот класс можно использовать внутри TaskApp.

# TODO: решение
class Menu:
    def show(self):
        print("\n" + "=" * 30)
        print("        МЕНЮ ЗАДАЧ")
        print("=" * 30)
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Отметить задачу как выполненную")
        print("0. Выход")
        print("-" * 30)

    def ask_choice(self):
        return input("Ваш выбор: ")


# Обновленный TaskApp с меню
class TaskAppWithMenu:
    def __init__(self, interface, menu):
        self.interface = interface
        self.menu = menu
        self.tasks = []

    def add_task(self):
        title = self.interface.ask_task_title()
        task = Task(title)
        self.tasks.append(task)
        self.interface.show_message(f"Задача '{title}' добавлена!")

    def show_all_tasks(self):
        if not self.tasks:
            self.interface.show_message("Список задач пуст.")
            return
        
        self.interface.show_message("\nСписок задач:")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. ", end="")
            self.interface.show_task(task)

    def mark_task_done(self):
        if not self.tasks:
            self.interface.show_message("Нет задач для отметки!")
            return
        
        self.show_all_tasks()
        try:
            index = int(input("Номер задачи для отметки: ")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].mark_done()
                self.interface.show_message("Задача отмечена как выполненная!")
            else:
                self.interface.show_message("Неверный номер!")
        except ValueError:
            self.interface.show_message("Введите число!")

    def run(self):
        while True:
            self.menu.show()
            choice = self.menu.ask_choice()
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.show_all_tasks()
            elif choice == "3":
                self.mark_task_done()
            elif choice == "0":
                self.interface.show_message("До свидания!")
                break
            else:
                self.interface.show_message("Неверный выбор! Попробуйте снова.")


# Пример использования
if __name__ == "__main__":
    # Простое приложение из задания 3
    print("=== Пример 1: Простое приветствие ===")
    interface = ConsoleUserInterface()
    app = App(interface)
    app.run()
    
    print("\n=== Пример 2: Менеджер задач ===")
    task_interface = ConsoleTaskInterface()
    menu = Menu()
    task_app = TaskAppWithMenu(task_interface, menu)
    task_app.run()