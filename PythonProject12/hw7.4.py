import sys
import time


class CommonElementsFinder:
    def find_common(self) -> set:
        multiples_of_3 = [x for x in range(100) if x % 3 == 0]
        multiples_of_5 = [x for x in range(100) if x % 5 == 0]

        set_3 = set(multiples_of_3)
        set_5 = set(multiples_of_5)

        return set_3.intersection(set_5)

    def display_result(self, result_set: set):
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"\n{BOLD}Пошук спільних елементів:{RESET}")

        sorted_list = sorted(list(result_set))
        result_str = str(sorted_list)

        prefix = "Перетин множин: "
        full_message = f"{prefix}{result_str}"

        for char in full_message:
            sys.stdout.write(f"{GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")


if __name__ == "__main__":
    finder = CommonElementsFinder()

    result = finder.find_common()
    finder.display_result(result)
