import string
import sys
import time


class LetterRangeExpander:
    def __init__(self):
        self.alphabet_map = string.ascii_letters

    def get_slice(self, query: str) -> str:
        start_char, end_char = query.split('-')

        start_index = self.alphabet_map.index(start_char)
        end_index = self.alphabet_map.index(end_char)

        return self.alphabet_map[start_index: end_index + 1]

    def display_result(self, result_string: str):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Діапазон розшифровано:{RESET}")

        for char in result_string:
            sys.stdout.write(f"{GREEN}{char}{RESET} ")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    expander = LetterRangeExpander()

    user_input = input("Введіть літери через дефіс (наприклад a-e): ")

    result = expander.get_slice(user_input)

    expander.display_result(result)
