def move_zeros_to_end_new(data_list):
    non_zeros = [x for x in data_list if x != 0]

    zeros = [0] * (len(data_list) - len(non_zeros))

    return non_zeros + zeros


test_lists = [
    ([0, 1, 0, 12, 3], [1, 12, 3, 0, 0]),
    ([0], [0]),
    ([1, 0, 13, 0, 0, 0, 5], [1, 13, 5, 0, 0, 0, 0]),
    ([9, 0, 7, 31, 0, 45, 0, 45, 0, 45, 0, 0, 96, 0], [9, 7, 31, 45, 45, 45, 96, 0, 0, 0, 0, 0, 0, 0]),
    ([], []),
    ([1, 2, 3], [1, 2, 3]),
    ([0, 0, 0], [0, 0, 0])
]

print("--- Метод 1: Створення Нового Списку ---")
for original, expected in test_lists:
    result = move_zeros_to_end_new(original)
    print(f"Було: {original} => Стало: {result} (Очікувано: {expected})")