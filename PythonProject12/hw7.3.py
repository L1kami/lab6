import sys
import time


class SecondIndexFinder:
    def second_index(self, text: str, symbol: str) -> int | None:
        if text.count(symbol) < 2:
            return None

        first_index = text.find(symbol)
        return text.find(symbol, first_index + 1)

    def display_result(self, result):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Результат пошуку:{RESET}")

        prefix = "Індекс другого входження: "
        full_message = f"{prefix}{result}"

        for char in full_message:
            sys.stdout.write(f"{GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    finder = SecondIndexFinder()

    text_input = input("Введіть основний рядок: ")
    symbol_input = input("Введіть рядок для пошуку: ")

    result = finder.second_index(text_input, symbol_input)
    finder.display_result(result)
