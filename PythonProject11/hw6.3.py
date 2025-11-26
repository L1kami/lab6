import sys
import time
from functools import reduce
from operator import mul


class DigitMultiplier:
    def process_number(self, number: int):
        current = abs(number)
        history = [current]

        while current > 9:
            digits = [int(d) for d in str(current)]
            current = reduce(mul, digits)
            history.append(current)

        return history

    def display_results(self, history: list):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Обчислення мультиплікативної стійкості:{RESET}")

        for i, val in enumerate(history):
            if i == 0:
                prefix = "Вхідне число: "
            elif i == len(history) - 1:
                prefix = "Результат:    "
            else:
                prefix = f"Крок {i}:       "

            message = f"{prefix}{val}"

            for char in message:
                sys.stdout.write(f"{GREEN}{char}{RESET}")
                sys.stdout.flush()
                time.sleep(0.04)
            print()
        print()


if __name__ == "__main__":
    multiplier = DigitMultiplier()

    try:
        user_input = int(input("Введіть ціле число: "))
        result_history = multiplier.process_number(user_input)
        multiplier.display_results(result_history)
    except ValueError:
        print("Будь ласка, введіть коректне ціле число.")
