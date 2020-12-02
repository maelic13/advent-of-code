from itertools import combinations
from numpy import prod
from typing import Optional

from src.infra.api import DataReader


def expense_record(file_name: str, number_of_items: int) -> Optional:
    data = DataReader.read_txt(file_name, int)
    for item in combinations(data, number_of_items):
        if check_addition(item, 2020):
            return prod(item)
    return None


def check_addition(iterable, target):
    return sum(iterable) == target


if __name__ == "__main__":
    solution = expense_record("d1_t1.txt", 2)
    print("Solution is: {}".format(solution))
