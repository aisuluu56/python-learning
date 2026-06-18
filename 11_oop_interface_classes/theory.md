# Тема 11. Классы для интерфейса

## Зачем нужны интерфейсные классы

В простых программах ввод, вывод и логика часто смешаны в одном месте.

```python
name = input("Имя: ")
print(f"Привет, {name}")
```

Для маленьких задач это нормально. Но когда программа растет, удобнее разделять:

- модель хранит данные и правила;
- интерфейс отвечает за общение с пользователем;
- приложение связывает части вместе.

## Пример модели

```python
class User:
    def __init__(self, name):
        self.name = name

    def get_greeting(self):
        return f"Привет, {self.name}"
```

Модель ничего не знает про `input()` и `print()`.

## Пример интерфейсного класса

```python
class ConsoleUserInterface:
    def ask_name(self):
        return input("Введите имя: ")

    def show_message(self, message):
        print(message)
```

Этот класс отвечает только за консольный интерфейс.

## Пример класса приложения

```python
class App:
    def __init__(self, interface):
        self.interface = interface

    def run(self):
        name = self.interface.ask_name()
        user = User(name)
        self.interface.show_message(user.get_greeting())
```

Запуск:

```python
interface = ConsoleUserInterface()
app = App(interface)
app.run()
```

## Почему это важно

Такой подход помогает в будущем заменить интерфейс.

Сегодня программа работает в консоли:

```python
interface = ConsoleUserInterface()
```

Позже можно сделать графический интерфейс или веб-интерфейс, но оставить модели почти без изменений.

## Классы для меню

Интерфейсный класс может показывать меню и возвращать выбор пользователя.

```python
class Menu:
    def show(self):
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("0. Выход")

    def ask_choice(self):
        return input("Выберите пункт: ")
```

## Разделение ответственности

Хорошее правило:

- модель не использует `input()` и `print()`;
- интерфейс не хранит сложные правила предметной области;
- класс приложения управляет сценарием работы.

Пример:

```python
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
        status = "готово" if task.is_done else "не готово"
        print(f"{task.title}: {status}")
```

Этот стиль пригодится, когда вы начнете писать классы для моделей и отдельно классы для интерфейса.
