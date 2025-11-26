import sys
import time


class PersonGreeter:
    def say_hi(self, name: str, age: int) -> str:
        return f"Hi. My name is {name} and I'm {age} years old"

    def display_greeting(self, message: str):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Система ідентифікації:{RESET}")

        prefix = "Вивід: "
        full_message = f"{prefix}{message}"

        for char in full_message:
            sys.stdout.write(f"{GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    greeter = PersonGreeter()

    try:
        user_name = input("Введіть ім'я: ")
        user_age = int(input("Введіть вік: "))

        if user_age > 0:
            result = greeter.say_hi(user_name, user_age)
            greeter.display_greeting(result)
        else:
            print("Вік має бути позитивним числом.")

    except ValueError:
        print("Вік має бути числом.")
