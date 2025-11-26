"""
Лабораторна робота №4: Моделювання Бензопили.

Модуль містить клас Benzopyla для представлення бензопили з її основними
технічними характеристиками та функцію main() для демонстрації
створення об'єктів та виведення їхніх даних.
"""


class Benzopyla:
    """
    Клас, що представляє об'єкт "Бензопила"

    Містить атрибути для назви, потужності та швидкості ланцюга.
    Встановлює загальні константи для категорії інструмента та гарантії.
    """

    TOOL_CATEGORY: str = "Садова техніка"
    DEFAULT_WARRANTY_MONTHS: int = 12

    def __init__(
        self, name: str = "N/A", power_watts: float = 0.0, chain_speed_rpm: int = 0
    ):
        """
        Конструктор класу Benzopyla.

        :param name: Назва моделі бензопили.
        :param power_watts: Потужність двигуна у ватах.
        :param chain_speed_rpm: Швидкість ланцюга в обертах за хвилину.
        """
        self.__name = name
        self.__power_watts = power_watts
        self.__chain_speed_rpm = chain_speed_rpm
        print(f"Створено об'єкт: {self.__name}")

    def __del__(self):
        """
        Деструктор. Виводиться повідомлення про видалення об'єкта.
        """
        print(f"Видалено об'єкт: {self.__name}")

    def get_name(self) -> str:
        """
        Повертає назву моделі бензопили.
        """
        return self.__name

    def get_power_watts(self) -> float:
        """
        Повертає потужність двигуна у ватах.
        """
        return self.__power_watts

    def get_chain_speed_rpm(self) -> int:
        """
        Повертає швидкість ланцюга в обертах за хвилину.
        """
        return self.__chain_speed_rpm

    def set_name(self, name: str):
        """
        Встановлює назву моделі. Якщо назва порожня, встановлює "N/A".

        :param name: Нова назва моделі.
        """
        self.__name = name if name else "N/A"

    def set_power_watts(self, power_watts: float):
        """
        Встановлює потужність двигуна. Не дозволяє від'ємних значень.

        :param power_watts: Нова потужність у ватах.
        """
        self.__power_watts = max(0.0, power_watts)

    def set_chain_speed_rpm(self, chain_speed_rpm: int):
        """
        Встановлює швидкість ланцюга. Не дозволяє від'ємних значень.

        :param chain_speed_rpm: Нова швидкість ланцюга.
        """
        self.__chain_speed_rpm = max(0, chain_speed_rpm)

    def __str__(self) -> str:
        """
        Повертає рядок для зручного виведення інформації про об'єкт.
        """
        return (
            f"Бензопила: {self.__name}\n"
            f"  ├ Потужність: {self.__power_watts} Вт\n"
            f"  └ Швидкість: {self.__chain_speed_rpm} об/хв"
        )

    def __repr__(self) -> str:
        """
        Повертає офіційне строкове представлення об'єкта.
        """
        return (
            f"Benzopyla(name='{self.__name}', "
            f"power_watts={self.__power_watts}, "
            f"chain_speed_rpm={self.__chain_speed_rpm})"
        )


def main():
    """
    Основна функція програми для демонстрації класу Benzopyla.

    Створює кілька об'єктів, додає їх до списку і виводить на екран
    детальні характеристики кожного інструмента.
    """
    print("--- Запуск програми ---\n")

    saw1 = Benzopyla()
    saw1.set_ojbb("Stihl MS 180")
    saw1.set_power_watts(1500.0)
    saw1.set_chain_speed_rpm(9000)

    saw2 = Benzopyla(name="Husqvarna 135", power_watts=1600.5, chain_speed_rpm=10500)

    saw3 = Benzopyla(name="Makita EA3201S", power_watts=1350.0, chain_speed_rpm=8800)

    saws = [saw1, saw2, saw3]
    print(f"\n--- Створено {len(saws)} шт. ---\n")

    for i, saw in enumerate(saws, 1):
        print(f"--- Дані по об'єкту #{i} ---")
        print(saw)

        print("  Поля через геттери:")
        print(f"    Назва: {saw.get_name()}")
        print(f"    Потужність: {saw.get_power_watts()}")
        print(f"    Оберти: {saw.get_chain_speed_rpm()}")

        print("  Загальні поля класу:")
        print(f"    Категорія: {saw.TOOL_CATEGORY}")
        print(f"    Гарантія: {saw.DEFAULT_WARRANTY_MONTHS} міс.\n")

    print("--- Завершення роботи ---")


if __name__ == "__main__":
    main()
