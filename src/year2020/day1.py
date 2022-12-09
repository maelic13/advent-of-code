from itertools import combinations

from numpy import prod

from src.infra import DataReader


def expense_record(item_list: list[int], number_of_items: int) -> int:
    for item in combinations(item_list, number_of_items):
        if sum(item) == 2020:
            return int(prod(item))
    raise RuntimeError("Solution not found!")


def advent1() -> None:
    data = DataReader.read_txt("day1.txt", int)
    solution1 = expense_record(data, 2)
    print(f"Solution part 1 is: {solution1}")

    solution2 = expense_record(data, 3)
    print(f"Solution part 2 is: {solution2}")


if __name__ == "__main__":
    advent1()
