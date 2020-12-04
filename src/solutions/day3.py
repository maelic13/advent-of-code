from math import gcd
import numpy as np
from typing import List

from src.infra.api import DataReader


def count_trees_hit(slope_map: List, current_pos: np.ndarray, slope: np.ndarray) -> int:
    slope = slope / gcd(slope[0], slope[1])
    trees_hit = 0
    while current_pos[1] < len(slope_map):
        x = int(current_pos[1])
        y = int(current_pos[0]) % len(slope_map[x])
        if slope_map[x][y] == "#":
            trees_hit += 1
        current_pos = np.add(current_pos, slope)
    return trees_hit


if __name__ == "__main__":
    input_data = DataReader.read_txt("day3_brother.txt", str)

    single_slope = np.array((3, 1))
    result = count_trees_hit(input_data, np.array((0, 0)), single_slope)
    print("With slope {} you hit {} trees.".format((3, 1), result))

    result_list = [result]
    slopes = [
        np.array((1, 1)),
        np.array((5, 1)),
        np.array((7, 1)),
        np.array((1, 2))
    ]
    for single_slope in slopes:
        result = count_trees_hit(input_data, np.array((0, 0)), single_slope)
        result_list.append(result)
    result_multi = np.prod(result_list)
    print("\nWith multiple additional slopes, result is {} trees.".format(result_multi))
    print("Step results are: {}".format(result_list))
