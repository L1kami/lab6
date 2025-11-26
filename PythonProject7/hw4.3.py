import random


def create_and_sample_list():
    num_elements = random.randint(3, 10)

    original_list = [random.randint(1, 100) for _ in range(num_elements)]

    first_element = original_list[0]

    third_element = original_list[2]

    second_from_end = original_list[-2]

    sampled_list = [first_element, third_element, second_from_end]

    print("--- Результати генерації ---")
    print(f"1. Довжина оригінального списку: {len(original_list)}")
    print(f"2. Оригінальний список: {original_list}")
    print(f"3. Вибрані елементи:")
    print(f"   - Перший (індекс 0): {first_element}")
    print(f"   - Третій (індекс 2): {third_element}")
    print(f"   - Другий з кінця (індекс -2): {second_from_end}")
    print(f"4. Результуючий список (новий): {sampled_list}")

    return original_list, sampled_list


if __name__ == "__main__":
    original, sampled = create_and_sample_list()