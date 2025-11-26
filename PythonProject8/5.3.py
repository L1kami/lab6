import string


def create_hashtag(input_string: str) -> str:
    translator = str.maketrans('', '', string.punctuation)

    cleaned_string = input_string.translate(translator).lower()

    words = [word for word in cleaned_string.split() if word]

    capitalized_words = [word.capitalize() for word in words]

    hashtag_body = "".join(capitalized_words)

    final_hashtag = "#" + hashtag_body

    MAX_LENGTH = 140

    if len(final_hashtag) > MAX_LENGTH:
        return final_hashtag[:MAX_LENGTH]

    return final_hashtag


# --- Приклади перевірки ---
print("--- Перевірка генератора хештегів ---")

test_1 = "Hello, world! this is a test string."
result_1 = create_hashtag(test_1)
print(f"Вхід: '{test_1}'\nВихід: {result_1}\n")

long_text = "a long string that needs to be truncated because it exceeds the maximum allowed length for a hashtag which is set at one hundred and forty characters. This will ensure proper compliance with social media standards."
result_2 = create_hashtag(long_text)
print(f"Вхід: (довгий текст) | Довжина: {len(result_2)}\nВихід: {result_2}\n")

test_3 = "  one TWO three   "
result_3 = create_hashtag(test_3)
print(f"Вхід: '{test_3}'\nВихід: {result_3}\n")

test_4 = ""
result_4 = create_hashtag(test_4)
print(f"Вхід: '{test_4}'\nВихід: {result_4}\n")

test_5 = "!!! - - ?"
result_5 = create_hashtag(test_5)
print(f"Вхід: '{test_5}'\nВихід: {result_5}\n")