def move_last_to_first_new(data_list):
    n = len(data_list)

    if n <= 1:
        return data_list

    return data_list[-1:] + data_list[:-1]


original_list = [10, 20, 30, 40]
new_list = move_last_to_first_new(original_list)
print(f"Оригінал [10, 20, 30, 40] -> {original_list}")
print(f"Новий список -> {new_list}")

