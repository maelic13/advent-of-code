from itertools import combinations
from time import time_ns

from numpy import prod


def expense_record(item_list: list[int], number_of_items: int) -> int:
    for item in combinations(item_list, number_of_items):
        if sum(item) == 2020:
            return int(prod(item))
    raise RuntimeError("Solution not found!")


def advent1() -> None:
    with open("inputs/2020/day1.txt", "r") as file:
        data = [int(line.strip()) for line in file.readlines()]

    solution1 = expense_record(data, 2)
    print(f"Solution part 1 is: {solution1}")

    solution2 = expense_record(data, 3)
    print(f"Solution part 2 is: {solution2}")


if __name__ == "__main__":
    start = time_ns()
    advent1()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
