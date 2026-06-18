# Этап 05. Экран каталога

## Задача экрана каталога

Экран каталога показывает пользователю доступные товары и помогает найти нужный.

Обычно на таком экране есть:

- таблица или список товаров;
- строка поиска;
- фильтры;
- сортировка;
- область с деталями выбранной позиции;
- кнопка добавления в корзину.

## Пример из другой области

В desktop-приложении для библиотеки экран каталога книг может содержать:

- таблицу книг;
- фильтр по жанру;
- поиск по названию;
- сортировку по году издания;
- кнопку "Забронировать".

Код обновления таблицы может выглядеть так:

```python
def refresh_books(self):
    for item_id in self.books_tree.get_children():
        self.books_tree.delete(item_id)

    books = self.library_service.find_books(
        title=self.search_var.get(),
        genre=self.genre_var.get(),
    )

    for book in books:
        self.books_tree.insert(
            "",
            "end",
            values=(book.title, book.genre, book.year),
        )
```

Экран не ищет книги сам. Он вызывает `library_service`.

## Treeview и идентификаторы

В таблице удобно показывать понятные пользователю данные, а внутри хранить идентификатор объекта.

Например:

```python
item_id = tree.insert("", "end", values=("Python", "Учебник", 2025))
row_to_book_id[item_id] = book.id
```

Когда пользователь выбирает строку, можно получить `book.id` и обратиться к сервису.

Выбор строки обычно обрабатывают через `bind()`.

```python
def on_book_selected(self, event):
    selected_rows = self.books_tree.selection()

    if not selected_rows:
        self.selected_book_id = None
        return

    row_id = selected_rows[0]
    self.selected_book_id = self.row_to_book_id[row_id]
    self.show_book_details(self.selected_book_id)


self.books_tree.bind("<<TreeviewSelect>>", self.on_book_selected)
```

Так пользователь видит обычные данные в таблице, а приложение хранит настоящий идентификатор объекта.

## Выбор размера

Для магазина одежды важно не просто выбрать товар, но и выбрать размер.

Размер лучше показывать отдельно:

- в `Combobox`;
- в списке доступных размеров;
- в блоке деталей выбранного товара.

Если размера нет в наличии, интерфейс должен показать понятную ошибку или не давать добавить товар.

## Количество и проверка ввода

Для числового выбора можно использовать `Spinbox`.

```python
ticket_count = tk.IntVar(value=1)

count_spinbox = ttk.Spinbox(
    root,
    from_=1,
    to=10,
    textvariable=ticket_count,
    width=5,
)
count_spinbox.pack()
```

Если используется обычный `Entry`, значение нужно преобразовать в число и обработать ошибку.

```python
try:
    count = int(count_var.get())
except ValueError:
    messagebox.showerror("Ошибка", "Количество должно быть числом")
    return

if count < 1:
    messagebox.showerror("Ошибка", "Количество должно быть больше нуля")
    return
```
