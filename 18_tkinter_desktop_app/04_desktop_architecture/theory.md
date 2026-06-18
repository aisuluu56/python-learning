# Этап 04. Архитектура desktop-приложения

## Почему GUI нужно отделять от логики

Desktop-интерфейс быстро становится сложным: окна, кнопки, таблицы, формы, сообщения. Если добавить туда SQL, расчеты скидок и оформление заказов, приложение станет трудно поддерживать.

Хороший слой интерфейса отвечает за три вещи:

- прочитать данные из виджетов;
- вызвать нужный метод сервиса;
- показать результат пользователю.

Он не должен решать, можно ли оформить заказ, как считать скидку или как уменьшать остатки.

## Пример из другой области

Представим приложение для записи пациентов в клинику.

Сервис:

```python
class AppointmentService:
    def __init__(self, schedule_repository):
        self.schedule_repository = schedule_repository

    def book(self, patient_name, doctor_id, date_time):
        if not patient_name:
            raise ValueError("Имя пациента обязательно")

        if not self.schedule_repository.is_free(doctor_id, date_time):
            raise ValueError("Время уже занято")

        return self.schedule_repository.create_appointment(
            patient_name,
            doctor_id,
            date_time,
        )
```

Интерфейс:

```python
def on_book_button_click():
    try:
        appointment = appointment_service.book(
            patient_name_var.get(),
            selected_doctor_id,
            date_time_var.get(),
        )
    except ValueError as error:
        messagebox.showerror("Ошибка", str(error))
        return

    messagebox.showinfo("Готово", f"Запись создана: {appointment.id}")
```

Интерфейс не знает, как устроено расписание. Он только вызывает сервис.

## Возможная структура классов

Для desktop-приложения удобно использовать несколько классов:

- `DesktopApp` - создает главное окно и хранит общие зависимости;
- `CatalogFrame` - экран каталога;
- `CartFrame` - экран корзины;
- `CheckoutFrame` - экран оформления заказа;
- `AppContainer` или `ScreenManager` - переключает экраны;
- `BackendFactory` - собирает репозитории и сервисы.

Не обязательно делать все сразу. Но уже на этом этапе важно перестать писать весь интерфейс в одном большом блоке.

## Переключение экранов

Один из простых способов навигации - хранить несколько `Frame` и показывать только нужный.

```python
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
```

Если экран должен обновляться перед показом, можно договориться о методе `refresh()`.

```python
def show_frame(self, name):
    for frame in self.frames.values():
        frame.pack_forget()

    frame = self.frames[name]

    if hasattr(frame, "refresh"):
        frame.refresh()

    frame.pack(fill="both", expand=True)
```

## Временные заглушки

Пока настоящий backend не готов, можно создать небольшие классы-заглушки с теми же методами, которые ожидает интерфейс.

```python
class FakeCourseService:
    def get_active_courses(self):
        return []
```

Это помогает разрабатывать интерфейс постепенно, а потом заменить заглушку настоящим сервисом.

## Импорт backend-кода

Если backend лежит в задании 17, desktop-слой должен импортировать его, а не копировать классы.

Из-за папок, начинающихся с цифр, может понадобиться `importlib.import_module()`.

```python
import importlib

cart_module = importlib.import_module(
    "17_clothing_store_project.05_cart.tasks"
)
```

В реальном проекте лучше вынести общий код в пакет с обычным именем, но для учебного курса такой прием допустим.
