def calculate_sum_and_multiply(data: list[int]) -> int:
    if not data:
        return 0

    sum_even_indices = sum(data[::2])

    last_element = data[-1]

    result = sum_even_indices * last_element

    return result


# --- Приклади для перевірки коректності ---

print("--- Перевірка: Сума парних індексів * Останній елемент ---")

list_a = [0, 1, 7, 2, 4, 8]
result_a = calculate_sum_and_multiply(list_a)
print(f"Список {list_a} => Результат: {result_a} (Очікувано: 88)")

list_b = [1, 3, 5]
result_b = calculate_sum_and_multiply(list_b)
print(f"Список {list_b} => Результат: {result_b} (Очікувано: 30)")

list_c = [6]
result_c = calculate_sum_and_multiply(list_c)
print(f"Список {list_c} => Результат: {result_c} (Очікувано: 36)")

list_d = []
result_d = calculate_sum_and_multiply(list_d)
print(f"Список {list_d} => Результат: {result_d} (Очікувано: 0)")