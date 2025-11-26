import sys
import time


class SentenceCorrector:
    def correct_sentence(self, text: str) -> str:
        if not text:
            return ""

        text = text[0].upper() + text[1:]

        if not text.endswith('.'):
            text += '.'

        return text

    def display_result(self, message: str):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Результат виправлення:{RESET}")

        prefix = "Вивід: "
        full_message = f"{prefix}{message}"

        for char in full_message:
            sys.stdout.write(f"{GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    corrector = SentenceCorrector()

    user_input = input("Введіть речення: ")

    result = corrector.correct_sentence(user_input)
    corrector.display_result(result)
