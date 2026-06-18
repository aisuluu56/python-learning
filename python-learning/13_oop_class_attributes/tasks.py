"""
Тема 13. Атрибуты класса и атрибуты объекта
"""


# Задание 1
# Создайте класс Course.
# У класса должен быть атрибут класса platform со значением "Stepik".
# В __init__ сохраните title как атрибут объекта.
# Создайте два курса и выведите их названия и platform.

# TODO: решение
class Course:
    platform = "Stepik"

    def __init__(self, title):
        self.title = title


course1 = Course("Python для начинающих")
course2 = Course("ООП на практике")

print(f"Курс: {course1.title}, Платформа: {course1.platform}")
print(f"Курс: {course2.title}, Платформа: {course2.platform}")
print(f"Атрибут класса: {Course.platform}")
print()


# Задание 2
# Создайте класс Ticket.
# У класса должен быть атрибут класса currency со значением "руб.".
# В __init__ сохраните event_name и price.
# Добавьте метод get_info(), который возвращает строку:
# Билет на <event_name>: <price> <currency>

# TODO: решение
class Ticket:
    currency = "руб."

    def __init__(self, event_name, price):
        self.event_name = event_name
        self.price = price

    def get_info(self):
        return f"Билет на {self.event_name}: {self.price} {self.currency}"


ticket1 = Ticket("Концерт", 2500)
ticket2 = Ticket("Театр", 1800)
print(ticket1.get_info())
print(ticket2.get_info())
print()


# Задание 3
# Создайте класс Visit.
# Добавьте атрибут класса total_visits со значением 0.
# При создании каждого объекта увеличивайте Visit.total_visits на 1.
# Создайте несколько посещений и выведите Visit.total_visits.

# TODO: решение
class Visit:
    total_visits = 0

    def __init__(self, visitor_name):
        self.visitor_name = visitor_name
        Visit.total_visits += 1


visit1 = Visit("Анна")
visit2 = Visit("Иван")
visit3 = Visit("Мария")

print(f"Всего посещений: {Visit.total_visits}")
print()


# Задание 4
# Создайте класс Delivery.
# Добавьте атрибуты класса STATUS_WAITING = "waiting" и STATUS_SENT = "sent".
# При создании доставки status должен быть STATUS_WAITING.
# Добавьте метод send(), который меняет status на STATUS_SENT.

# TODO: решение
class Delivery:
    STATUS_WAITING = "waiting"
    STATUS_SENT = "sent"

    def __init__(self, order_id):
        self.order_id = order_id
        self.status = self.STATUS_WAITING

    def send(self):
        self.status = self.STATUS_SENT

    def get_info(self):
        return f"Заказ #{self.order_id}: {self.status}"


delivery1 = Delivery(1001)
delivery2 = Delivery(1002)

print(delivery1.get_info())
print(delivery2.get_info())

delivery1.send()
print(f"После отправки: {delivery1.get_info()}")
print()


# Задание 5
# Создайте класс Laptop.
# У класса должен быть атрибут класса warranty_months.
# У объекта должны быть model и owner.
# Создайте несколько ноутбуков и покажите, что warranty_months общий для всех.

# TODO: решение
class Laptop:
    warranty_months = 24

    def __init__(self, model, owner):
        self.model = model
        self.owner = owner


laptop1 = Laptop("MacBook Pro", "Алексей")
laptop2 = Laptop("ThinkPad X1", "Екатерина")
laptop3 = Laptop("Dell XPS", "Дмитрий")

print(f"{laptop1.owner}: {laptop1.model}, гарантия {laptop1.warranty_months} мес.")
print(f"{laptop2.owner}: {laptop2.model}, гарантия {laptop2.warranty_months} мес.")
print(f"{laptop3.owner}: {laptop3.model}, гарантия {laptop3.warranty_months} мес.")

# Доказываем, что атрибут общий
print(f"\nАтрибут класса Laptop.warranty_months = {Laptop.warranty_months}")

# Меняем через класс
Laptop.warranty_months = 36
print(f"После изменения: гарантия стала {laptop1.warranty_months} мес. для всех")
print()


# Задание 6
# Создайте класс Message.
# У класса должен быть атрибут total_sent.
# Каждый новый объект увеличивает total_sent.
# Добавьте метод get_total_sent(), который возвращает общее количество созданных сообщений.

# TODO: решение
class Message:
    total_sent = 0

    def __init__(self, text, sender):
        self.text = text
        self.sender = sender
        Message.total_sent += 1

    def get_total_sent(self):
        return Message.total_sent

    @classmethod
    def get_total_sent_cls(cls):
        return cls.total_sent


msg1 = Message("Привет!", "Анна")
msg2 = Message("Как дела?", "Иван")
msg3 = Message("Отлично!", "Мария")

print(f"Сообщение 1 от {msg1.sender}: {msg1.text}")
print(f"Сообщение 2 от {msg2.sender}: {msg2.text}")
print(f"Сообщение 3 от {msg3.sender}: {msg3.text}")
print(f"Всего отправлено сообщений: {msg3.get_total_sent()}")
print(f"Всего отправлено (через класс): {Message.total_sent}")
print()


# Дополнительная демонстрация важной особенности
print("=" * 50)
print("ВАЖНАЯ ОСОБЕННОСТЬ:")
print("=" * 50)


class Product:
    currency = "руб."


book = Product()
phone = Product()

book.currency = "долл."  # Создаётся атрибут объекта

print(f"book.currency: {book.currency}")      # долл. (атрибут объекта)
print(f"phone.currency: {phone.currency}")    # руб. (атрибут класса)
print(f"Product.currency: {Product.currency}") # руб. (атрибут класса)