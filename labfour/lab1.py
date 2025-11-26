"""
Модуль для демонстрації класу Benzopyla.

Містить клас Benzopyla та приклад його використання
для створення та відображення об'єктів.
"""


class Benzopyla:
    """
    Клас, що представляє об'єкт 'Бензопила'.

    Атрибути:
        vyrobnyk (str): Публічне поле, виробник бензопили.
        rik_vypusku (int): Публічне поле, рік випуску.
    """
    vyrobnyk = ""
    rik_vypusku = 0

    def __init__(self, nazva=None, potuzhnist=0, kilkist_obertiv=0):
        """
        Конструктор класу Benzopyla.

        Args:
            nazva (str, optional): Назва моделі. Defaults to None.
            potuzhnist (int, optional): Потужність у ватах. Defaults to 0.
            kilkist_obertiv (int, optional): Оберти ланцюга. Defaults to 0.
        """
        self.__nazva = nazva
        self.__potuzhnist = potuzhnist
        self.__kilkist_obertiv = kilkist_obertiv

    def __del__(self):
        """Деструктор, виводить повідомлення при видаленні об'єкта."""
        print(f"Пилку {self.__nazva} видалено")

    def get_nazva(self):
        """Повертає приватне поле 'nazva'."""
        return self.__nazva

    def get_potuzhnist(self):
        """Повертає приватне поле 'potuzhnist'."""
        return self.__potuzhnist

    def get_kilkist_obertiv(self):
        """Повертає приватне поле 'kilkist_obertiv'."""
        return self.__kilkist_obertiv

    def __str__(self):
        """Повертає рядок для зручного виведення інформації про об'єкт."""
        return (f"Бензопила: {self.__nazva} "
                f"(Виробник: {self.vyrobnyk}, {self.__potuzhnist} Вт)")

    def __repr__(self):
        """Повертає офіційне строкове представлення об'єкта."""
        return (f"Benzopyla('{self.__nazva}', "
                f"{self.__potuzhnist}, {self.__kilkist_obertiv})")


def main():
    """
    Основна функція для демонстрації роботи класу.

    Створює три об'єкти класу Benzopyla та виводить
    інформацію про їхні поля.
    """
    pyla1 = Benzopyla()
    pyla1.vyrobnyk = "Noname"
    pyla1.rik_vypusku = 2020

    pyla2 = Benzopyla("MS 180", 1500, 9000)
    pyla2.vyrobnyk = "Stihl"
    pyla2.rik_vypusku = 2023

    pyla3 = Benzopyla("135 Mark II", 1600, 9000)
    pyla3.vyrobnyk = "Husqvarna"
    pyla3.rik_vypusku = 2022

    print("\n--- Інформація про пилки ---")

    print("\nПилка 1:")
    print(f"  Назва: {pyla1.get_nazva()}")
    print(f"  Потужність: {pyla1.get_potuzhnist()} Вт")
    print(f"  Оберти: {pyla1.get_kilkist_obertiv()} об/хв")
    print(f"  Виробник: {pyla1.vyrobnyk}")
    print(f"  Рік: {pyla1.rik_vypusku}")

    print("\nПилка 2:")
    print(f"  Назва: {pyla2.get_nazva()}")
    print(f"  Потужність: {pyla2.get_potuzhnist()} Вт")
    print(f"  Оберти: {pyla2.get_kilkist_obertiv()} об/хв")
    print(f"  Виробник: {pyla2.vyrobnyk}")
    print(f"  Рік: {pyla2.rik_vypusku}")

    print("\nПилка 3:")
    print(f"  Назва: {pyla3.get_nazva()}")
    print(f"  Потужність: {pyla3.get_potuzhnist()} Вт")
    print(f"  Оберти: {pyla3.get_kilkist_obertiv()} об/хв")
    print(f"  Виробник: {pyla3.vyrobnyk}")
    print(f"  Рік: {pyla3.rik_vypusku}")

    print("\n--- Використання str i repr ---")
    print(f"str: {pyla2}")
    print(f"repr: {repr(pyla3)}")

    print("\n--- Кінець програми (деструктори) ---")


if __name__ == "__main__":
    main()
