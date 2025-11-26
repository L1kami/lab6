import math


def safe_input(prompt, type_func=float):
    while True:
        try:
            user_input = input(prompt).replace(',', '.')
            return type_func(user_input)
        except ValueError:
            print("Помилка: Введіть коректне число.")


def calculator():
    print("Простий Калькулятор Python")
    print("Підтримувані операції: +, -, *, /")
    print("-" * 30)

    is_running = True
    while is_running:

        num1 = safe_input("Введіть перше число (a): ")

        while True:
            operation = input("Введіть операцію (+, -, *, /): ").strip()
            if operation in ('+', '-', '*', '/'):
                break
            print("Помилка: Непідтримувана операція. Спробуйте ще раз.")

        num2 = safe_input("Введіть друге число (b): ")

        result = None

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                print("\nПОМИЛКА: Ділення на нуль неможливе.")
                result = None
            else:
                result = num1 / num2

        if result is not None:
            print(f"\nРезультат: {num1} {operation} {num2} = {result}")

        print("-" * 30)

        continue_choice = input("Продовжити роботу калькулятора? (yes/no або будь-що інше для виходу): ").strip().lower()

        if continue_choice not in ('yes', 'y'):
            is_running = False
            print("Робота калькулятора завершена.")

        print("-" * 30)


if __name__ == "__main__":
    calculator()