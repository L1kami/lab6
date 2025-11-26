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
    print("Для завершення роботи введіть 'exit' або 'вихід' замість операції.")
    print("-" * 30)

    while True:
        num1 = safe_input("Введіть перше число (a): ")

        operation = input("Введіть операцію (+, -, *, /): ").strip()

        if operation.lower() in ('exit', 'вихід'):
            print("Робота калькулятора завершена.")
            break

        if operation not in ('+', '-', '*', '/'):
            print("Помилка: Непідтримувана операція. Спробуйте ще раз.")
            continue

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
                print("\nПОМИЛКА: Ділення на нуль неможливе. Спробуйте ще раз.")
                print("-" * 30)
                continue
            result = num1 / num2

        if result is not None:
            print(f"\nРезультат: {num1} {operation} {num2} = {result}")

        print("-" * 30)


if __name__ == "__main__":
    calculator()