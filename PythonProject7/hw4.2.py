def checkio(data):
    if not data:
        return 0

    sum_even_indices = sum(data[::2])

    last_element = data[-1]

    result = sum_even_indices * last_element

    return result



print("--- Перевірка: Сума парних індексів, помножена на останній елемент ---")

list_a = [0, 1, 2, 3, 4, 5]
result_a = checkio(list_a)
print(f"Список {list_a} | Результат: {result_a}")

list_b = [1, 3, 5, 7, 9]
result_b = checkio(list_b)
print(f"Список {list_b} | Результат: {result_b}")

list_c = [5]
result_c = checkio(list_c)
print(f"Список {list_c} | Результат: {result_c}")

list_d = []
result_d = checkio(list_d)
print(f"Список {list_d} | Результат: {result_d}")