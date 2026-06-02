# Этап 02. Компоновка и виджеты

## Зачем нужна компоновка

В desktop-приложении элементы нужно размещать аккуратно: заголовки, кнопки, поля ввода, таблицы и панели не должны накладываться друг на друга.

В `tkinter` чаще всего используют:

- `pack()` - размещение блоками сверху, снизу, слева или справа;
- `grid()` - размещение по строкам и столбцам;
- `place()` - размещение по точным координатам.

Для учебного приложения обычно хватает `pack()` и `grid()`. `place()` лучше использовать редко, потому что интерфейс хуже адаптируется к изменению размера окна.

## Frame как контейнер

`Frame` помогает разделять окно на области.

Пример из другой области: приложение для учета учебных курсов.

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

filters_frame = ttk.Frame(root)
filters_frame.pack(fill="x", padx=10, pady=10)

table_frame = ttk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(filters_frame, text="Преподаватель").grid(row=0, column=0)
teacher_entry = ttk.Entry(filters_frame)
teacher_entry.grid(row=0, column=1)

root.mainloop()
```

Один контейнер отвечает за фильтры, другой - за таблицу. Так код становится понятнее.

Если используется `grid()`, строкам и столбцам можно задать вес. Тогда нужная область будет растягиваться при изменении размера окна.

```python
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

table_frame.grid(row=1, column=0, sticky="nsew")
```

Параметр `sticky="nsew"` растягивает виджет к северу, югу, западу и востоку внутри ячейки.

## ttk-виджеты

Модуль `tkinter.ttk` содержит более современные версии стандартных элементов:

- `ttk.Button`;
- `ttk.Label`;
- `ttk.Entry`;
- `ttk.Combobox`;
- `ttk.Treeview`;
- `ttk.Frame`.

Для таблиц особенно полезен `Treeview`.

```python
columns = ("title", "author")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("title", text="Название")
tree.heading("author", text="Автор")

tree.insert("", "end", values=("Python Basics", "A. Ivanov"))
tree.pack(fill="both", expand=True)
```

Для выпадающего списка используют `Combobox`.

```python
genre_box = ttk.Combobox(
    root,
    values=("Все жанры", "Учебники", "Романы"),
    state="readonly",
)
genre_box.set("Все жанры")
genre_box.pack()
```

Ширину колонок таблицы можно настроить отдельно.

```python
tree.column("title", width=220)
tree.column("author", width=160)
```

## Правило для интерфейса

Каждый экран лучше собирать из небольших областей:

- верхняя панель действий;
- основная область данных;
- нижняя панель статуса или итогов.

Такой подход пригодится для каталога, корзины и оформления заказа.
