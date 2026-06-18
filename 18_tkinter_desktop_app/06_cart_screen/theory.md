# Этап 06. Экран корзины

## Что должен делать экран корзины

Корзина показывает товары, которые пользователь собирается купить.

Обычно на экране корзины есть:

- список позиций;
- название товара;
- размер;
- цена за единицу;
- количество;
- сумма по позиции;
- итоговая сумма;
- кнопки изменения количества и удаления.

## Пример из другой области

В приложении заказа билетов экран выбранных билетов может показывать:

- мероприятие;
- сектор;
- место;
- цену;
- итоговую сумму.

Интерфейс не должен сам пересчитывать сложные правила скидок. Он вызывает сервис или объект корзины.

```python
def refresh_tickets(self):
    self.ticket_tree.delete(*self.ticket_tree.get_children())

    for item in self.cart.get_items():
        self.ticket_tree.insert(
            "",
            "end",
            values=(item.event_title, item.seat, item.price),
        )

    self.total_var.set(f"{self.cart.get_total()} руб.")
```

Если нужно сохранить связь между строкой таблицы и объектом корзины, можно использовать словарь.

```python
self.row_to_ticket_id = {}

row_id = self.ticket_tree.insert(
    "",
    "end",
    values=(item.event_title, item.seat, item.price),
)
self.row_to_ticket_id[row_id] = item.id
```

## Обновление количества

Количество можно менять разными способами:

- отдельным полем ввода;
- кнопками "+" и "-";
- `Spinbox`;
- диалоговым окном.

Главное правило: после изменения количества таблица и итоговая сумма должны обновиться.

Пример обработки выбранной позиции:

```python
def get_selected_ticket_id(self):
    selected_rows = self.ticket_tree.selection()

    if not selected_rows:
        messagebox.showerror("Ошибка", "Выберите билет")
        return None

    row_id = selected_rows[0]
    return self.row_to_ticket_id[row_id]
```

После изменения данных нужно снова вызвать метод обновления таблицы.

```python
ticket_id = self.get_selected_ticket_id()

if ticket_id is None:
    return

self.cart.change_quantity(ticket_id, new_quantity)
self.refresh_tickets()
```

## Подтверждение действий

Перед очисткой всего списка лучше спросить подтверждение.

```python
from tkinter import messagebox

confirmed = messagebox.askyesno(
    "Подтверждение",
    "Очистить список выбранных билетов?",
)

if confirmed:
    self.cart.clear()
    self.refresh_tickets()
```

## Ошибки корзины

Интерфейс должен аккуратно обрабатывать ситуации:

- корзина пуста;
- позиция не выбрана;
- введено не число;
- количество меньше 1;
- товара не хватает на складе.

Для пользователя это должны быть обычные сообщения, а не traceback в консоли.
