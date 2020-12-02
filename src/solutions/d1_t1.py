from itertools import combinations
from numpy import ndarray, prod
from typing import Callable, Iterable, Optional

from src.infra.api import DataReader


def expense_record(file_name: str, number_of_items: int) -> Optional[ndarray]:
    data = DataReader.read_txt(file_name, int)
    for item in combinations(data, number_of_items):
        if check_item(item, sum, 2020):
            return prod(item)
    return None


def check_item(iterable: Iterable, function: Callable, target: float) -> bool:
    return function(iterable) == target


if __name__ == "__main__":
    solution = expense_record("d1_t1.txt", 2)
    print("Solution is: {}".format(solution))
