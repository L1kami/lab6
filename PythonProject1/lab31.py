"""
 A dominator is a value that occurs in more than half of the elements.
"""

def find_dominator(arr):
    """
    Finds a dominator in a list of numbers.

    A dominator is a value that occurs in more than half of the elements.
    """
    if not arr:
        return -1

    counts = {}
    for number in arr:
        if number in counts:
            counts[number] += 1
        else:
            counts[number] = 1

    threshold = len(arr) / 2

    for number, count in counts.items():
        if count > threshold:
            return number

    return -1


list1 = [3, 4, 3, 2, 3, 1, 3, 3]
dominator1 = find_dominator(list1)
print(f"Послідовність: {list1}")
print(f"Домінатор: {dominator1}")

print("-" * 20)

list2 = []
dominator2 = find_dominator(list2)
print(f"Послідовність: {list2}")
print(f"Домінатор: {dominator2}")

print("-" * 20)

list3 = [1, 2, 3, 4, 5, 6]
dominator3 = find_dominator(list3)
print(f"Послідовність: {list3}")
print(f"Домінатор: {dominator3}")

print("-" * 20)

list4 = [2, 2, 1, 1]
dominator4 = find_dominator(list4)
print(f"Послідовність: {list4}")
print(f"Домінатор: {dominator4}")