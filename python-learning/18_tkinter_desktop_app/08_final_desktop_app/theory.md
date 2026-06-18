# Этап 08. Итоговое desktop-приложение

## Что значит собрать приложение

На предыдущих этапах были созданы отдельные части интерфейса: каталог, корзина, оформление заказа. Теперь их нужно соединить в одно приложение.

Финальное desktop-приложение должно иметь:

- главное окно;
- навигацию между экранами;
- общий доступ к сервисам;
- единый стиль виджетов;
- обработку ошибок;
- понятный сценарий покупки.

## Пример из другой области

В desktop-приложении для учебного центра могут быть экраны:

- список курсов;
- заявка на обучение;
- профиль студента;
- история заявок.

Главный класс приложения создает сервисы и передает их экранам:

```python
class EducationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.course_service = CourseService(...)
        self.registration_service = RegistrationService(...)

        self.course_frame = CourseFrame(self.root, self.course_service)
        self.registration_frame = RegistrationFrame(
            self.root,
            self.registration_service,
        )
```

Экраны не создают сервисы сами. Они получают готовые зависимости.

## Сборка зависимостей

Создание сервисов лучше держать в одном месте. Тогда экраны получают готовые объекты и не знают, как именно они устроены.

```python
def build_services():
    course_repository = CourseRepository()
    course_service = CourseService(course_repository)
    registration_service = RegistrationService(course_repository)

    return {
        "course_service": course_service,
        "registration_service": registration_service,
    }
```

В учебном проекте магазина такой функцией можно собрать репозитории, сервис каталога, корзину, сервис заказов и сервис скидок.

## Навигация

Навигацию можно сделать по-разному:

- верхнее меню;
- панель кнопок;
- вкладки `ttk.Notebook`;
- переключение `Frame`.

Для учебного приложения достаточно панели кнопок или `Notebook`.

Перед показом экрана можно вызвать его `refresh()`, если такой метод есть.

```python
def show_screen(self, name):
    frame = self.frames[name]

    if hasattr(frame, "refresh"):
        frame.refresh()

    frame.tkraise()
```

Для варианта с `tkraise()` все экраны обычно заранее размещают в одной ячейке.

```python
for frame in self.frames.values():
    frame.grid(row=0, column=0, sticky="nsew")
```

## Стиль и размер окна

Минимальный размер защищает интерфейс от слишком сильного сжатия.

```python
root.geometry("1000x650")
root.minsize(800, 500)
```

Для `ttk` можно настроить общий стиль.

```python
style = ttk.Style()
style.configure("TButton", padding=6)
style.configure("Treeview", rowheight=26)
```

## Проверка итогового сценария

Перед сдачей нужно пройти путь пользователя от начала до конца:

1. Запуск приложения.
2. Просмотр каталога.
3. Поиск товара.
4. Добавление в корзину.
5. Изменение количества.
6. Оформление заказа.
7. Сообщение об успешном результате.

Если приложение работает только при идеальном вводе, оно еще не готово. Нужно проверить ошибочные сценарии.
