from time import time

from regex import findall


def is_id_invalid(i: int) -> bool:
    id_string = str(i)
    if len(id_string) % 2 != 0:
        return False

    return id_string[: len(id_string) // 2] == id_string[len(id_string) // 2 :]


def is_id_invalid_2(number: int) -> bool:
    id_string = str(number)
    match = findall(r"^(.+)\1+$", id_string)
    return bool(match)


def day2() -> None:
    with open("inputs/2025/day2.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # part 1
    invalid_ids: set[int] = set()
    for string in lines[0].strip().split(","):
        begin, end = string.split("-")
        for i in range(int(begin), int(end) + 1):
            if i in invalid_ids:
                continue
            if is_id_invalid(i):
                invalid_ids.add(i)
    print(sum(invalid_ids))

    # part 2
    invalid_ids: set[int] = set()
    for string in lines[0].strip().split(","):
        begin, end = string.split("-")
        for i in range(int(begin), int(end) + 1):
            if i in invalid_ids:
                continue
            if is_id_invalid_2(i):
                invalid_ids.add(i)
    print(sum(invalid_ids))


if __name__ == "__main__":
    start = time()
    day2()
    print(f"Execution time: {round((time() - start), 1)} seconds.")
