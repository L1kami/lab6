"""
 A dominator is a value that occurs in more than half of the elements.
"""

def find_dominator(arr):
    """
    Finds a dominator in a list of numbers.

    A dominator is a value that occurs in more than half of the elements.
    """
    dominator = -1

    counts = {}
    for number in arr:
        if number in counts:
            counts[number] += 1
        else:
            counts[number] = 1

    if arr:
        threshold = len(arr) / 2

        for number, count in counts.items():
            if count > threshold:
                dominator = number
                break

    return dominator


list1 = [3, 4, 3, 2, 3, 1, 3, 3]
list11 = []
dominator1 = find_dominator(list11)
print(f"Послідовність: {list11}")
print(f"Домінатор: {dominator1}")

print("-" * 20)

list2 = [1, 2, 3, 4, 5, 6]
dominator2 = find_dominator(list2)
print(f"Послідовність: {list2}")
print(f"Домінатор: {dominator2}")

print("-" * 20)

list3 = [2, 2, 1, 1]
dominator3 = find_dominator(list3)
print(f"Послідовність: {list3}")
print(f"Домінатор: {dominator3}")
