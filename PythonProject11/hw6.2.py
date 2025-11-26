import sys
import time


class TimeConverter:
    def convert(self, total_seconds: int) -> str:
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        day_word = self._get_day_declension(days)

        time_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

        return f"{days} {day_word}, {time_str}"

    def _get_day_declension(self, days: int) -> str:
        if 11 <= days % 100 <= 14:
            return "днів"

        last_digit = days % 10

        if last_digit == 1:
            return "день"
        elif 2 <= last_digit <= 4:
            return "дні"
        else:
            return "днів"

    def display_result(self, formatted_time: str):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Час конвертовано:{RESET}")

        for char in formatted_time:
            sys.stdout.write(f"{GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    converter = TimeConverter()

    try:
        user_input = int(input("Введіть кількість секунд (0 - 8640000): "))

        if 0 <= user_input < 8640000:
            result = converter.convert(user_input)
            converter.display_result(result)
        else:
            print("Число виходить за межі дозволеного діапазону!")

    except ValueError:
        print("Будь ласка, введіть ціле число.")