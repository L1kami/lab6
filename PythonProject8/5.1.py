import keyword
import string


def is_valid_pirate_name(name: str) -> bool:
    if name in keyword.kwlist:
        return False

    if not name:
        return False

    if name[0].isdigit():
        return False

    if any(c.isupper() for c in name):
        return False

    forbidden_symbols = string.punctuation.replace('_', '') + ' '
    if any(char in forbidden_symbols for char in name):
        return False

    if name.count('_') > 1:
        return False

    return True


print("--- Перевірка: Імена Змінних One Piece ---")

print(f"luffy_gear: {is_valid_pirate_name('luffy_gear')} (True)")
print(f"haki: {is_valid_pirate_name('haki')} (True)")
print(f"bounty7: {is_valid_pirate_name('bounty7')} (True)")
print(f"devil_fruit: {is_valid_pirate_name('devil_fruit')} (True)")

print("-" * 20)

print(f"9ships: {is_valid_pirate_name('9ships')} (False)")
print(f"StrawHat: {is_valid_pirate_name('StrawHat')} (False)")
print(f"zoro sword: {is_valid_pirate_name('zoro sword')} (False)")
print(f"marine-ford: {is_valid_pirate_name('marine-ford')} (False)")
print(f"if: {is_valid_pirate_name('if')} (False)")
print(f"for: {is_valid_pirate_name('for')} (False)")
print(f"sea__king: {is_valid_pirate_name('sea__king')} (False)")
print(f"one_piece_log: {is_valid_pirate_name('one_piece_log')} (False)")