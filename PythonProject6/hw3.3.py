def split_list_into_two(original_list):
    n = len(original_list)

    if n == 0:
        return [[], []]

    split_index = (n + 1) // 2

    list1 = original_list[:split_index]
    list2 = original_list[split_index:]

    return [list1, list2]



print("--- Перевірка: Розділення списку на два ---")

empty_list = []
result_empty = split_list_into_two(empty_list)
print(f"Порожній список {empty_list} => {result_empty}")

even_list = [10, 20, 30, 40]
result_even = split_list_into_two(even_list)
print(f"Парна довжина {even_list} => {result_even}")

odd_list = [1, 2, 3, 4, 5]
result_odd = split_list_into_two(odd_list)
print(f"Непарна довжина {odd_list} => {result_odd}")

single_list = ['a']
result_single = split_list_into_two(single_list)
print(f"Один елемент {single_list} => {result_single}")