class Benzopyla:
    TOOL_CATEGORY: str = "Садова техніка"
    DEFAULT_WARRANTY_MONTHS: int = 12

    def __init__(
            self, name: str = "N/A", power_watts: float = 0.0, chain_speed_rpm: int = 0
    ):
        self.__name = name if name else "N/A"

        self.set_power_watts(power_watts)
        self.set_chain_speed_rpm(chain_speed_rpm)

        print(f"Створено об'єкт: {self.__name}")

    def __del__(self):
        print(f"Видалено об'єкт: {self.__name}")

    def get_name(self) -> str:
        return self.__name

    def get_power_watts(self) -> float:
        return self.__power_watts

    def get_chain_speed_rpm(self) -> int:
        return self.__chain_speed_rpm

    def set_name(self, name: str):
        self.__name = name if name else "N/A"

    def set_power_watts(self, power_watts: float):
        self.__power_watts = max(0.0, power_watts)

    def set_chain_speed_rpm(self, chain_speed_rpm: int):
        self.__chain_speed_rpm = max(0, chain_speed_rpm)

    def __str__(self) -> str:
        return (
            f"Бензопила: {self.__name}\n"
            f"  ├ Потужність: {self.__power_watts} Вт\n"
            f"  └ Швидкість: {self.__chain_speed_rpm} об/хв"
        )

    def __repr__(self) -> str:
        return (
            f"Benzopyla(name='{self.__name}', "
            f"power_watts={self.__power_watts}, "
            f"chain_speed_rpm={self.__chain_speed_rpm})"
        )


def main():
    print("--- Запуск програми ---\n")

    saw1 = Benzopyla()
    saw1.set_name("Stihl MS 180")
    saw1.set_power_watts(1500.0)
    saw1.set_chain_speed_rpm(9000)

    saw2 = Benzopyla(name="Husqvarna 135", power_watts=1600.5, chain_speed_rpm=10500)

    saw3 = Benzopyla(name="Makita EA3201S", power_watts=-1350.0, chain_speed_rpm=-8800)

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