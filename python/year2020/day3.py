from math import gcd, prod
from time import time_ns

import numpy as np


def count_trees_hit(slope_map: list[str], current_pos: np.ndarray, slope: np.ndarray) -> int:
    slope = slope / gcd(slope[0], slope[1])
    trees_hit = 0
    while current_pos[1] < len(slope_map):
        x_index = int(current_pos[1])
        y_index = int(current_pos[0]) % len(slope_map[x_index])
        if slope_map[x_index][y_index] == "#":
            trees_hit += 1
        current_pos = np.add(current_pos, slope)
    return trees_hit


def advent3() -> None:
    with open("inputs/2020/day3.txt", "r") as file:
        data = file.readlines()

    single_slope = np.array((3, 1))
    result = count_trees_hit(data, np.array((0, 0)), single_slope)
    print(f"With slope {(3, 1)} you hit {result} trees.")

    result_list = [result]
    slopes = [
        np.array((1, 1)),
        np.array((5, 1)),
        np.array((7, 1)),
        np.array((1, 2))
    ]
    for single_slope in slopes:
        result = count_trees_hit(data, np.array((0, 0)), single_slope)
        result_list.append(result)
    result_multi = prod(result_list)
    print(f"\nWith multiple additional slopes, result is {result_multi} trees.")
    print(f"Step results are: {result_list}")


if __name__ == "__main__":
    start = time_ns()
    advent3()
    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
