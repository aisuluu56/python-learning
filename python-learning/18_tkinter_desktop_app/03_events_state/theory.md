# Этап 03. События и состояние

## Что такое событие

Событие - это действие пользователя или системы:

- клик по кнопке;
- ввод текста;
- выбор строки в таблице;
- закрытие окна;
- нажатие клавиши.

В `tkinter` событие связывается с функцией-обработчиком.

```python
def add_book():
    print("Книга добавлена")

button = ttk.Button(root, text="Добавить", command=add_book)
```

Функция `add_book` вызовется только после клика по кнопке.

## Переменные интерфейса

Для связи виджетов с данными используются специальные переменные:

- `StringVar` - строка;
- `IntVar` - целое число;
- `BooleanVar` - логическое значение;
- `DoubleVar` - число с дробной частью.

Пример из другой области: форма записи на курс.

```python
student_name = tk.StringVar()

entry = ttk.Entry(root, textvariable=student_name)
entry.pack()

def show_name():
    print(student_name.get())

button = ttk.Button(root, text="Показать", command=show_name)
button.pack()
```

Метод `.get()` получает значение, `.set()` изменяет его.

## Обновление интерфейса

После действия пользователя интерфейс часто нужно обновить:

- очистить таблицу;
- добавить новую строку;
- изменить текст статуса;
- показать ошибку.

Для сообщений удобно использовать `messagebox`.

```python
from tkinter import messagebox

messagebox.showinfo("Готово", "Запись сохранена")
messagebox.showerror("Ошибка", "Заполните имя")
```

Таблицу `Treeview` перед повторным заполнением обычно очищают.

```python
for row_id in tree.get_children():
    tree.delete(row_id)
```

После этого можно добавить новые строки через `insert()`.

## Выбор строки в таблице

Выбор строки тоже является событием. Его можно обработать через `bind()`.

```python
def on_book_selected(event):
    selected_rows = tree.selection()

    if not selected_rows:
        return

    selected_row = selected_rows[0]
    values = tree.item(selected_row, "values")
    status_var.set(f"Выбрана книга: {values[0]}")


tree.bind("<<TreeviewSelect>>", on_book_selected)
```

`selection()` возвращает выбранные строки, а `item(row_id, "values")` возвращает значения выбранной строки.

## Строка статуса

Статус удобно хранить в `StringVar` и показывать через `Label`.

```python
status_var = tk.StringVar(value="Готово")
status_label = ttk.Label(root, textvariable=status_var)
status_label.pack(fill="x")
```

## Состояние приложения

Состояние - это данные, которые приложение помнит между действиями пользователя.

Например, в приложении бронирования кабинетов состояние может хранить:

- выбранный кабинет;
- выбранную дату;
- список найденных броней;
- текущего пользователя.

В магазине таким состоянием станут выбранный товар, выбранный размер и корзина.

Важно: состояние интерфейса не должно заменять бизнес-логику. Интерфейс хранит то, что нужно для отображения, а правила покупки должны оставаться в сервисах.
