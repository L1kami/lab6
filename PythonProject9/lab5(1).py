from enum import Enum


class NegativeValueError(Exception):
    pass


class MovieType(Enum):
    BOYOVICK = "boyovick"
    COMEDY = "comedy"
    HORROR = "horror"
    DRAMA = "drama"
    FANTASY = "fantasy"


class Movie:
    def __init__(self, id, title, ranking, release_date, character_number, ticket_price, comment, movie_type):
        if id < 0:
            raise NegativeValueError(f"ID не може бути від'ємним. Отримано: {id}")
        if ranking < 0:
            raise NegativeValueError(f"Рейтинг не може бути від'ємним. Отримано: {ranking}")
        if character_number < 0:
            raise NegativeValueError(f"Кількість персонажів не може бути від'ємною. Отримано: {character_number}")
        if ticket_price < 0:
            raise NegativeValueError(f"Ціна квитка не може бути від'ємною. Отримано: {ticket_price}")

        if not (0 <= ranking <= 10):
            raise ValueError(f"Рейтинг має бути в межах від 0 до 10. Отримано: {ranking}")

        self._id = id
        self._title = title
        self._ranking = ranking
        self._release_date = release_date
        self._character_number = character_number
        self._ticket_price = ticket_price
        self._comment = comment
        self._movie_type = movie_type

        print(f"СТВОРЕНО ФІЛЬМ: {self._title}")

    def __del__(self):
        try:
            print(f"ВИДАЛЕНО ФІЛЬМ: {self._title}")
        except AttributeError:
            pass

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, new_ranking):
        if new_ranking < 0:
            raise NegativeValueError(f"Рейтинг не може бути від'ємним. Отримано: {new_ranking}")

        if 0 <= new_ranking <= 10:
            self._ranking = new_ranking
        else:
            raise ValueError(f"Рейтинг має бути в межах від 0 до 10. Отримано: {new_ranking}")

    @property
    def release_date(self):
        return self._release_date

    @property
    def character_number(self):
        return self._character_number

    @character_number.setter
    def character_number(self, new_number):
        if new_number < 0:
            raise NegativeValueError(f"Кількість персонажів не може бути від'ємною. Отримано: {new_number}")
        self._character_number = new_number

    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, new_price):
        if new_price < 0:
            raise NegativeValueError(f"Ціна квитка не може бути від'ємною. Отримано: {new_price}")
        self._ticket_price = new_price

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, new_comment):
        self._comment = new_comment

    @property
    def movie_type(self):
        return self._movie_type

    def display_info(self):
        print(f"""
ID: {self.id}
Назва: {self.title}
Жанр: {self.movie_type.value}
Рейтинг: {self.ranking}
Дата виходу: {self.release_date}
Кількість персонажів: {self.character_number}
Ціна квитка: {self.ticket_price}
Коментар: {self.comment}
""")


class Cinema:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.movies = []
        print(f"Кінотеатр '{self.name}' відкрито")

    def __del__(self):
        print(f"Кінотеатр '{self.name}' зачинено")

    def add_movie(self, movie):
        self.movies.append(movie)

    def show_movies(self):
        print(f"\nФільми у кінотеатрі '{self.name}':")
        for m in self.movies:
            m.display_info()

    def calculate_profit(self, movie, day_tickets_sold):
        if movie in self.movies:
            profit = day_tickets_sold * movie.ticket_price
            print(f"Прибуток '{movie.title}' за день: {profit} гривень")
        else:
            print(f"Фільм '{movie.title}' не знайдено у цьому кінотеатрі.")

    def choose_movie_by_rating(self, min_rating):
        filtered = [m for m in self.movies if m.ranking >= min_rating]
        print(f"\nФільми з рейтингом {min_rating} і вище:")
        for f in filtered:
            print(f" - {f.title} ({f.ranking})")
        return filtered

    def sort_movies_by_release(self):
        self.movies.sort(key=lambda m: m.release_date)
        print("\nФільми відсортовано за датою виходу.")

    def filter_movies(self, min_year=0, min_rating=0, min_price=0):
        """
        Фільтрує фільми за трьома параметрами з логікою 'від вказаного до максимуму'.
        За замовчуванням параметри 0, щоб не фільтрувати, якщо значення не передано.
        """
        print(f"\n--- ФІЛЬТР: Рік >= {min_year}, Рейтинг >= {min_rating}, Ціна >= {min_price} ---")

        filtered_list = []
        for m in self.movies:
            if (m.release_date >= min_year and
                    m.ranking >= min_rating and
                    m.ticket_price >= min_price):
                filtered_list.append(m)

        if not filtered_list:
            print("Фільмів за такими критеріями не знайдено.")
        else:
            for m in filtered_list:
                print(f" - {m.title} | Рік: {m.release_date} | Рейтинг: {m.ranking} | Ціна: {m.ticket_price}")

        return filtered_list


def main():
    print("--- Створення коректних об'єктів ---")
    try:
        m1 = Movie(1, "Re:Zero", 9.1, 2014, 34, 299, "Переродження", MovieType.FANTASY)
        m2 = Movie(2, "Justice League", 9.1, 2020, 74, 200, "Страхіття", MovieType.HORROR)
        m3 = Movie(3, "One Piece", 7.1, 2016, 432, 10, "Затягнутість", MovieType.FANTASY)
        m4 = Movie(4, "Interstellar", 8.8, 2014, 10, 150, "Космос", MovieType.DRAMA)
    except (NegativeValueError, ValueError) as e:
        print(f"Помилка при створенні фільму: {e}")
        return

    cinema = Cinema("Multiplex", "Львів Spartak")

    cinema.add_movie(m1)
    cinema.add_movie(m2)
    cinema.add_movie(m3)
    cinema.add_movie(m4)

    cinema.show_movies()


    cinema.filter_movies(min_year=2016)

    cinema.filter_movies(min_year=2014, min_rating=9.0)

    cinema.filter_movies(min_year=2014, min_rating=8.0, min_price=200)

    print("\n--- Інші методи ---")
    cinema.sort_movies_by_release()
    cinema.calculate_profit(m2, day_tickets_sold=120)

    print("\n--- Тести на помилки ---")
    try:
        Movie(-4, "Bad Movie", 5.0, 2025, 10, 100, "Тест", MovieType.COMEDY)
    except NegativeValueError as e:
        print(f"ЗЛОВЛЕНО ПОМИЛКУ: {e}")


if __name__ == "__main__":
    main()