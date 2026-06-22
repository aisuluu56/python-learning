"""
================================================================
МДК 01.01 Практическое задание
Приложение для учёта задач с графическим интерфейсом Tkinter
и хранением данных в PostgreSQL.

Реализовано монолитно (все компоненты в одном файле) для
простоты проверки.

Каждая строка кода прокомментирована с привязкой к темам
из предоставленной теории.
================================================================
"""

# ================================================================
# ИНСТРУКЦИЯ ПО УСТАНОВКЕ НЕОБХОДИМЫХ БИБЛИОТЕК
# (всё устанавливаем локально в корневую папку проекта)
# ================================================================
#
# 1. Откройте терминал в папке с этим файлом.
# 2. Выполните команду:
#    python -m pip install --target . psycopg2-binary pytest
#    (если python не находится, используйте полный путь, например
#    C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe -m pip install --target . psycopg2-binary pytest)
#
#    Параметр --target . означает "установить библиотеки прямо сюда,
#    в корень проекта".
# 3. После установки появятся папки psycopg2/, pytest/ и др.
# 4. Установите и запустите PostgreSQL, создайте базу taskdb
#    (подробнее см. комментарии в функции main()).
# 5. Запустите приложение: python app.py
# 6. Запустите тесты: python -m pytest app.py -v
# ================================================================

# ------------------------------------------------------------------
# Блок 1: Импорт библиотек и настройка путей для локальных модулей
# Соответствует темам: "Переменные", "Функции", "Модули".
# ------------------------------------------------------------------

import sys      # Тема 1: переменная sys — доступ к системным параметрам
import os       # Тема 1: работа с файловой системой

# Добавляем корневую папку проекта в sys.path, чтобы Python находил
# библиотеки, установленные через --target . (Тема 8: функции, os.path)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Теперь импортируем необходимые библиотеки.
# psycopg2 — драйвер PostgreSQL (Тема 2: импорт модулей)
import psycopg2

# tkinter — стандартная библиотека для GUI (Тема 11: классы для интерфейса)
import tkinter as tk
# messagebox — диалоговые окна, ttk — улучшенные виджеты (Treeview)
from tkinter import messagebox, ttk

# pytest — фреймворк для тестирования (Тема 8: функции, тесты)
import pytest


# ------------------------------------------------------------------
# Блок 2: SQL-скрипт для создания таблицы tasks
# Соответствует Этапу 02 (PostgreSQL) и Темам 5 (строки), 6 (списки? нет)
# ------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,          -- автоинкрементный ключ
    title TEXT NOT NULL,            -- название задачи (строка)
    status TEXT NOT NULL CHECK (status IN ('Новая', 'Выполнена'))
);
"""
# IF NOT EXISTS — безопасное создание (Тема 3: условия, если таблицы нет)
# SERIAL — целочисленный тип с автоувеличением (Тема 1: int)
# CHECK — ограничение на допустимые статусы (Тема 3: логическое условие)


# ------------------------------------------------------------------
# Блок 3: Модель Task (доменная модель)
# Соответствует Темам 9, 10 (классы, модели) и Этапу 01.
# ------------------------------------------------------------------

class Task:
    """
    Класс-модель для хранения данных одной задачи.
    Не содержит SQL-запросов, только атрибуты и методы представления.
    """

    def __init__(self, task_id, title, status):
        """
        Конструктор (Тема 9: __init__, self).
        :param task_id: int или None (для новой задачи)
        :param title: str
        :param status: str ('Новая' или 'Выполнена')
        """
        # Тема 1: присваивание значений атрибутам объекта
        self.id = task_id
        self.title = title
        self.status = status

    def __repr__(self):
        """
        Магический метод __repr__ (Тема 14) — строковое представление
        для разработчика, удобно при отладке.
        """
        # Тема 5: f-строка для форматирования
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"


# ------------------------------------------------------------------
# Блок 4: Репозиторий TaskRepository (работа с PostgreSQL)
# Соответствует Этапу 03, Темам 12 (инкапсуляция), 6 (списки), 5 (строки).
# ------------------------------------------------------------------

class TaskRepository:
    """
    Класс-репозиторий отвечает за все SQL-запросы к таблице tasks.
    Использует psycopg2 и параметризованные запросы.
    """

    def __init__(self, db_params):
        """
        Конструктор (Тема 9).
        :param db_params: dict с ключами host, port, database, user, password
        """
        # Тема 7: словарь db_params хранит параметры подключения
        self.db_params = db_params
        # При создании репозитория сразу создаём таблицу, если её нет
        self._create_table_if_not_exists()

    def _get_connection(self):
        """
        Внутренний метод (инкапсуляция, Тема 12) для получения
        соединения с БД. Использует ** распаковку словаря (Тема 7).
        """
        # psycopg2.connect(**self.db_params) — передача параметров из словаря
        return psycopg2.connect(**self.db_params)

    def _create_table_if_not_exists(self):
        """
        Создаёт таблицу tasks, если она ещё не существует.
        Использует контекстный менеджер with (Тема 8: менеджеры контекста).
        """
        # with гарантирует закрытие соединения даже при ошибке
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Тема 5: выполнение SQL-строки
                cur.execute(CREATE_TABLE_SQL)
            # conn.commit() выполняется автоматически при выходе из with

    def add(self, task):
        """
        Добавляет новую задачу в БД (Тема 8: функция с параметрами).
        :param task: объект Task (без id)
        :return: Task с присвоенным id
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Параметризованный запрос (Тема 5: строки с %s)
                # Возвращает сгенерированный id через RETURNING
                cur.execute(
                    "INSERT INTO tasks (title, status) VALUES (%s, %s) RETURNING id;",
                    (task.title, task.status)  # кортеж значений (Тема 6: кортеж)
                )
                new_id = cur.fetchone()[0]  # извлекаем id (Тема 6: индексация кортежа)
            conn.commit()  # фиксируем транзакцию
        # Создаём новый объект Task с полученным id
        return Task(new_id, task.title, task.status)

    def get_all(self):
        """
        Возвращает список всех задач (Тема 8: функция, Тема 6: список).
        :return: list[Task]
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, status FROM tasks ORDER BY id;")
                rows = cur.fetchall()  # список кортежей (Тема 6)
        # Генератор списка: превращаем каждый кортеж в объект Task (Тема 4: цикл)
        return [Task(row[0], row[1], row[2]) for row in rows]

    def update_status(self, task_id, status):
        """
        Обновляет статус задачи по id (Тема 8: функция с параметрами).
        :param task_id: int
        :param status: str ('Новая' или 'Выполнена')
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Параметризованный UPDATE
                cur.execute(
                    "UPDATE tasks SET status = %s WHERE id = %s;",
                    (status, task_id)
                )
            conn.commit()


# ------------------------------------------------------------------
# Блок 5: Сервис TaskService (бизнес-логика)
# Соответствует Этапу 04, Темам 12 (абстракция), 3 (условия).
# ------------------------------------------------------------------

class TaskService:
    """
    Сервис содержит правила предметной области:
    - название не может быть пустым;
    - новая задача получает статус 'Новая';
    - статус можно менять только на 'Новая' или 'Выполнена'.
    Работает с репозиторием через интерфейс (полиморфизм, Тема 12).
    """

    # Атрибут класса (Тема 13) — общий для всех экземпляров
    ALLOWED_STATUSES = ('Новая', 'Выполнена')  # Тема 6: кортеж

    def __init__(self, repository):
        """
        Конструктор (Тема 9).
        :param repository: объект с методами add, get_all, update_status
        """
        self.repo = repository  # композиция (Тема 12)

    def add_task(self, title):
        """
        Добавляет новую задачу (Тема 8).
        :param title: str
        :return: Task
        :raises ValueError: если title пустой или из пробелов
        """
        # Тема 3: условие if not title or not title.strip()
        if not title or not title.strip():
            raise ValueError("Название задачи не может быть пустым.")
        # Создаём задачу с временным id=None и статусом 'Новая'
        new_task = Task(None, title.strip(), 'Новая')
        return self.repo.add(new_task)

    def get_all_tasks(self):
        """Возвращает список всех задач (Тема 8)."""
        return self.repo.get_all()

    def complete_task(self, task_id):
        """Отмечает задачу как выполненную (Тема 8)."""
        self.repo.update_status(task_id, 'Выполнена')

    def update_task_status(self, task_id, status):
        """
        Универсальный метод смены статуса с проверкой допустимости.
        :raises ValueError: если статус не в ALLOWED_STATUSES
        """
        # Тема 3: проверка вхождения в кортеж
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Недопустимый статус: {status}. "
                f"Допустимые: {', '.join(self.ALLOWED_STATUSES)}"
            )
        self.repo.update_status(task_id, status)


# ------------------------------------------------------------------
# Блок 6: Графический интерфейс на Tkinter (класс TaskApp)
# Соответствует Темам 11, Этапам 05–08.
# ------------------------------------------------------------------

class TaskApp:
    """
    Главное окно приложения. Не содержит SQL-запросов, работает только
    через сервис. Реализует события (Тема 11: события).
    """

    def __init__(self, root, service):
        """
        Конструктор (Тема 9).
        :param root: корневое окно tk.Tk()
        :param service: объект TaskService
        """
        self.root = root
        self.service = service
        # Тема 1: заголовок окна — строка
        self.root.title("Учёт задач")

        # Переменная для хранения ID выбранной задачи (Тема 1: int)
        self.selected_task_id = None

        # Создаём все виджеты (Тема 11: методы класса)
        self._create_widgets()

        # При запуске сразу загружаем список (Тема 8: вызов метода)
        self.refresh_list()

    def _create_widgets(self):
        """
        Создаёт все элементы интерфейса: поле ввода, кнопки, таблицу.
        Соответствует Темам 11 и Этапу 02 по tkinter.
        """
        # --- Верхняя панель: поле ввода + кнопка "Добавить" ---
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)  # отступы (Тема 11: компоновка)

        # Тема 11: Label — текстовая метка
        tk.Label(frame_top, text="Название задачи:").pack(side=tk.LEFT, padx=5)
        # Entry — поле ввода (Тема 11: виджеты)
        self.entry_title = tk.Entry(frame_top, width=40)
        self.entry_title.pack(side=tk.LEFT, padx=5)
        # Кнопка с командой (Тема 11: событие command)
        btn_add = tk.Button(frame_top, text="Добавить", command=self.add_task)
        btn_add.pack(side=tk.LEFT, padx=5)

        # --- Таблица (Treeview) для отображения задач ---
        frame_list = tk.Frame(self.root)
        frame_list.pack(pady=10)

        # ttk.Treeview — таблица с колонками (Тема 11: ttk)
        self.tree = ttk.Treeview(
            frame_list,
            columns=("id", "title", "status"),
            show="headings",
            height=15
        )
        # Заголовки и ширина колонок
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("status", text="Статус")
        self.tree.column("id", width=50)
        self.tree.column("title", width=300)
        self.tree.column("status", width=100)
        self.tree.pack(side=tk.LEFT)

        # Скроллбар (Тема 11: Scrollbar)
        scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Событие выбора строки в таблице (Тема 11: bind)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- Нижняя панель: кнопки управления ---
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=10)

        btn_complete = tk.Button(
            frame_bottom,
            text="Отметить выполненной",
            command=self.complete_task
        )
        btn_complete.pack(side=tk.LEFT, padx=5)

        btn_refresh = tk.Button(
            frame_bottom,
            text="Обновить список",
            command=self.refresh_list
        )
        btn_refresh.pack(side=tk.LEFT, padx=5)

        # Информационная метка (Тема 11: Label)
        self.lbl_selected = tk.Label(self.root, text="Выбрано: нет", fg="gray")
        self.lbl_selected.pack(pady=5)

    def refresh_list(self):
        """
        Обновляет содержимое таблицы, загружая данные из сервиса.
        Соответствует Темам 4 (цикл for), 6 (список), 11 (обновление интерфейса).
        """
        # Очищаем все строки таблицы (Тема 4: цикл for)
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Получаем список задач через сервис (Тема 8)
            tasks = self.service.get_all_tasks()
            # Тема 4: цикл for по задачам
            for task in tasks:
                # Вставляем строку в конец (tk.END), values — кортеж (Тема 6)
                self.tree.insert("", tk.END, values=(task.id, task.title, task.status))
        except Exception as e:
            # Тема 11: messagebox для ошибок
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")

    def add_task(self):
        """
        Обработчик кнопки "Добавить".
        Проверяет ввод (Тема 3: условие) и вызывает сервис.
        """
        # Тема 5: strip() убирает пробелы по краям
        title = self.entry_title.get().strip()
        if not title:  # Тема 3: условие
            messagebox.showwarning("Предупреждение", "Название задачи не может быть пустым.")
            return

        try:
            self.service.add_task(title)
            self.entry_title.delete(0, tk.END)  # очищаем поле (Тема 6: удаление)
            self.refresh_list()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить задачу: {e}")

    def on_tree_select(self, event):
        """
        Обработчик события выбора строки (Тема 11: bind).
        Сохраняет ID выбранной задачи.
        """
        selected = self.tree.selection()  # список выбранных элементов (Тема 6)
        if selected:
            values = self.tree.item(selected[0], "values")  # кортеж значений
            if values:
                # Тема 1: преобразование строки в int
                self.selected_task_id = int(values[0])
                # Тема 5: f-строка для обновления метки
                self.lbl_selected.config(text=f"Выбрано: ID {self.selected_task_id} - {values[1]}")
            else:
                self.selected_task_id = None
                self.lbl_selected.config(text="Выбрано: нет")
        else:
            self.selected_task_id = None
            self.lbl_selected.config(text="Выбрано: нет")

    def complete_task(self):
        """
        Обработчик кнопки "Отметить выполненной".
        Проверяет, выбрана ли задача (Тема 3: условие).
        """
        if self.selected_task_id is None:
            messagebox.showwarning("Предупреждение", "Сначала выберите задачу из списка.")
            return

        try:
            self.service.complete_task(self.selected_task_id)
            self.refresh_list()
            # Сбрасываем выбор
            self.selected_task_id = None
            self.lbl_selected.config(text="Выбрано: нет")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить статус: {e}")


# ------------------------------------------------------------------
# Блок 7: Имитационный репозиторий для тестов (Mock)
# Соответствует Темам 12 (полиморфизм), 6 (списки), 8 (функции).
# ------------------------------------------------------------------

class MockTaskRepository:
    """
    Заглушка репозитория, хранит данные в оперативной памяти.
    Используется в тестах, чтобы не подключаться к реальной БД.
    """

    def __init__(self):
        self.tasks = []      # список задач (Тема 6)
        self._next_id = 1    # счётчик для генерации id (Тема 1: int)

    def add(self, task):
        """Добавляет задачу в память, присваивая id (Тема 8)."""
        # Создаём новую задачу с присвоенным id
        new_task = Task(self._next_id, task.title, task.status)
        self.tasks.append(new_task)   # добавляем в список (Тема 6)
        self._next_id += 1
        return new_task

    def get_all(self):
        """Возвращает копию списка задач (Тема 8, Тема 6: срез)."""
        return self.tasks.copy()   # защита от внешнего изменения

    def update_status(self, task_id, status):
        """Обновляет статус задачи по id (Тема 4: цикл for)."""
        for t in self.tasks:
            if t.id == task_id:
                t.status = status
                return


# ------------------------------------------------------------------
# Блок 8: Unit-тесты с использованием pytest
# Соответствует Темам 8 (функции), 3 (условия), 4 (циклы? нет),
# Этапу тестирования.
# ------------------------------------------------------------------

def test_add_task_success():
    """
    Тест 1: успешное добавление задачи (Тема 8: тест-функция).
    """
    # Создаём заглушку и сервис (Тема 9: создание объектов)
    mock_repo = MockTaskRepository()
    service = TaskService(mock_repo)

    # Добавляем задачу
    task = service.add_task("Написать отчёт")
    # Тема 3: утверждения assert (проверка условий)
    assert task.id is not None
    assert task.title == "Написать отчёт"
    assert task.status == "Новая"

    # Проверяем, что задача сохранилась в репозитории
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].title == "Написать отчёт"


def test_add_task_empty_title_raises_value_error():
    """
    Тест 2: ValueError при пустом названии (Тема 8, Тема 3: обработка исключений).
    """
    mock_repo = MockTaskRepository()
    service = TaskService(mock_repo)

    # pytest.raises проверяет, что возникло нужное исключение (Тема 3)
    with pytest.raises(ValueError, match="Название задачи не может быть пустым."):
        service.add_task("")
    with pytest.raises(ValueError, match="Название задачи не может быть пустым."):
        service.add_task("   ")


def test_update_status_invalid_status_raises_value_error():
    """
    Тест 3: ValueError при недопустимом статусе.
    """
    mock_repo = MockTaskRepository()
    service = TaskService(mock_repo)

    # Добавляем задачу, чтобы был id
    task = service.add_task("Тестовая задача")
    task_id = task.id

    with pytest.raises(ValueError, match="Недопустимый статус: Завершена"):
        service.update_task_status(task_id, "Завершена")

    # Проверяем, что статус не изменился
    tasks = service.get_all_tasks()
    assert tasks[0].status == "Новая"


# Дополнительный тест (четвёртый) — для полноты
def test_complete_task_success():
    """Тест 4: успешное выполнение задачи."""
    mock_repo = MockTaskRepository()
    service = TaskService(mock_repo)

    task = service.add_task("Сделать уборку")
    task_id = task.id

    service.complete_task(task_id)
    tasks = service.get_all_tasks()
    assert tasks[0].status == "Выполнена"


# ------------------------------------------------------------------
# Блок 9: Точка входа в приложение
# ------------------------------------------------------------------

def main():
    """
    Запускает GUI-приложение (Тема 8: функция).
    """
    # Параметры подключения к PostgreSQL (Тема 7: словарь)
    # ВНИМАНИЕ: замените пароль, имя базы, пользователя на свои!
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'taskdb',      # база данных, которую вы создали
        'user': 'postgres',
        'password': 'password'     # пароль, заданный при установке PostgreSQL
    }

    # Создаём реальный репозиторий и сервис (Тема 9: объекты)
    repo = TaskRepository(db_params)
    service = TaskService(repo)

    # Создаём окно Tkinter и запускаем (Тема 11)
    root = tk.Tk()
    app = TaskApp(root, service)   # app не используется напрямую, но объект живёт
    root.mainloop()                # главный цикл обработки событий


# Если файл запущен как основной (а не импортирован как модуль) (Тема 8)
if __name__ == "__main__":
    main()