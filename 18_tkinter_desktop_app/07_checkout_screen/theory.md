# Этап 07. Оформление заказа

## Что такое экран оформления

Экран оформления заказа собирает данные, необходимые для покупки:

- имя покупателя;
- телефон или email;
- адрес доставки;
- промокод;
- комментарий к заказу;
- подтверждение состава корзины.

Интерфейс должен помочь пользователю заполнить форму и показать понятные ошибки.

## Пример из другой области

В приложении записи на экзамен форма может собирать:

- имя студента;
- группу;
- предмет;
- дату;
- комментарий.

Валидация не должна быть только визуальной. Если имя пустое или дата неверная, сервис тоже должен уметь отказать.

```python
def on_submit(self):
    if not self.name_var.get().strip():
        messagebox.showerror("Ошибка", "Введите имя")
        return

    try:
        registration = self.exam_service.register(
            student_name=self.name_var.get(),
            group=self.group_var.get(),
            exam_id=self.selected_exam_id,
        )
    except ValueError as error:
        messagebox.showerror("Ошибка", str(error))
        return

    messagebox.showinfo("Готово", f"Заявка #{registration.id} создана")
```

## Валидация в интерфейсе

Интерфейс может заранее проверять простые ошибки:

- поле пустое;
- количество не является числом;
- email явно не похож на email;
- телефон слишком короткий.

Но окончательное решение лучше оставлять сервису, потому что один и тот же заказ может оформляться через desktop, web или API.

## Форма через grid

Форму удобно строить через `grid()`: подпись в первом столбце, поле ввода во втором.

```python
ttk.Label(form_frame, text="Имя").grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(form_frame, textvariable=name_var)
name_entry.grid(row=0, column=1, sticky="ew")

ttk.Label(form_frame, text="Группа").grid(row=1, column=0, sticky="w")
group_entry = ttk.Entry(form_frame, textvariable=group_var)
group_entry.grid(row=1, column=1, sticky="ew")

form_frame.columnconfigure(1, weight=1)
```

## Обновление сводки

Экран оформления часто показывают после других действий пользователя. Поэтому ему полезен метод `refresh()`, который перечитывает актуальные данные.

```python
def refresh(self):
    self.summary_tree.delete(*self.summary_tree.get_children())

    for item in self.cart.get_items():
        self.summary_tree.insert("", "end", values=(item.title, item.price))

    self.total_var.set(f"{self.cart.get_total()} руб.")
```

Так итоговая сумма не устаревает, если пользователь изменил корзину и снова вернулся к оформлению.

## Диалоги

Для оформления заказа полезны:

- `messagebox.showinfo()` - успешное оформление;
- `messagebox.showerror()` - ошибка;
- `messagebox.askyesno()` - подтверждение действия.

После успешного заказа корзину обычно очищают, а пользователя возвращают в каталог или на экран подтверждения.
