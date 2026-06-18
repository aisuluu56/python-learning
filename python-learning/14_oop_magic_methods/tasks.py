"""
Тема 14. Магические методы
"""


# Задание 1
# Создайте класс City с атрибутами name и population.
# Добавьте метод __str__(), который возвращает:
# Город <name>, население: <population>
# Создайте город и выведите его через print().

# TODO: решение
class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population

    def __str__(self):
        return f"Город {self.name}, население: {self.population}"


city = City("Москва", 12500000)
print(city)
print()


# Задание 2
# Создайте класс Movie с атрибутами title и year.
# Добавьте метод __repr__(), который возвращает строку:
# Movie(title='<title>', year=<year>)
# Проверьте вывод объекта.

# TODO: решение
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __repr__(self):
        return f"Movie(title='{self.title}', year={self.year})"


movie = Movie("Начало", 2010)
print(repr(movie))
print(movie)  # print использует __repr__, если нет __str__
print()


# Задание 3
# Создайте класс Point с атрибутами x и y.
# Добавьте метод __eq__(), чтобы две точки считались равными,
# если у них одинаковые x и y.
# Проверьте сравнение двух объектов через ==.

# TODO: решение
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


point1 = Point(3, 5)
point2 = Point(3, 5)
point3 = Point(7, 2)

print(f"point1 == point2: {point1 == point2}")  # True
print(f"point1 == point3: {point1 == point3}")  # False
print()


# Задание 4
# Создайте класс Playlist.
# Внутри храните список songs.
# Добавьте метод add_song(song).
# Добавьте метод __len__(), чтобы len(playlist) возвращал количество песен.

# TODO: решение
class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)


playlist = Playlist()
playlist.add_song("Bohemian Rhapsody")
playlist.add_song("Imagine")
playlist.add_song("Hey Jude")

print(f"Количество песен в плейлисте: {len(playlist)}")
print()


# Задание 5
# Создайте класс Package с атрибутами code и weight.
# Добавьте метод __lt__(), чтобы посылки сравнивались по весу.
# Проверьте выражение package1 < package2.

# TODO: решение
class Package:
    def __init__(self, code, weight):
        self.code = code
        self.weight = weight

    def __lt__(self, other):
        if not isinstance(other, Package):
            return NotImplemented
        return self.weight < other.weight

    def __repr__(self):
        return f"Package(code={self.code}, weight={self.weight}кг)"


package1 = Package("A001", 2.5)
package2 = Package("B002", 5.0)
package3 = Package("C003", 1.8)

print(f"{package1} < {package2}: {package1 < package2}")  # True (2.5 < 5.0)
print(f"{package2} < {package3}: {package2 < package3}")  # False (5.0 < 1.8)
print(f"{package3} < {package1}: {package3 < package1}")  # True (1.8 < 2.5)

# Сортировка списка посылок по весу
packages = [package1, package2, package3]
packages.sort()
print(f"Отсортировано по весу: {packages}")
print()


# Задание 6
# Создайте класс Wallet с атрибутами owner и amount.
# Добавьте __str__(), который возвращает:
# Кошелек <owner>: <amount> руб.
# Добавьте __eq__(), который сравнивает кошельки по owner и amount.

# TODO: решение
class Wallet:
    def __init__(self, owner, amount):
        self.owner = owner
        self.amount = amount

    def __str__(self):
        return f"Кошелек {self.owner}: {self.amount} руб."

    def __eq__(self, other):
        if not isinstance(other, Wallet):
            return False
        return self.owner == other.owner and self.amount == other.amount


wallet1 = Wallet("Анна", 5000)
wallet2 = Wallet("Анна", 5000)
wallet3 = Wallet("Иван", 3000)

print(wallet1)
print(wallet2)
print(wallet3)

print(f"wallet1 == wallet2: {wallet1 == wallet2}")  # True
print(f"wallet1 == wallet3: {wallet1 == wallet3}")  # False
print()


# Дополнительная демонстрация всех магических методов
print("=" * 50)
print("ДЕМОНСТРАЦИЯ ВСЕХ МЕТОДОВ ВМЕСТЕ")
print("=" * 50)


class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f"'{self.title}' - {self.author}"

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        return self.pages < other.pages

    def __len__(self):
        return self.pages


book1 = Book("1984", "Джордж Оруэлл", 328)
book2 = Book("1984", "Джордж Оруэлл", 328)
book3 = Book("Мастер и Маргарита", "Михаил Булгаков", 512)

print(f"__str__: {book1}")
print(f"__repr__: {repr(book1)}")
print(f"__eq__: {book1 == book2}")  # True
print(f"__lt__: {book1 < book3}")   # True (328 < 512)
print(f"__len__: {len(book1)} страниц")