from itertools import combinations
from numpy import ndarray, prod
from typing import Callable, Iterable, Optional

from src.infra.api import DataReader


def expense_record(item_list: Iterable, number_of_items: int) -> Optional[ndarray]:
    for item in combinations(item_list, number_of_items):
        if check_item(item, sum, 2020):
            return prod(item)
    return None


def check_item(iterable: Iterable, function: Callable, target: float) -> bool:
    return function(iterable) == target


if __name__ == "__main__":
    data = DataReader.read_txt("d1_t1.txt", int)
    solution = expense_record(data, 2)
    print("Solution is: {}".format(solution))
