from math import gcd
import numpy as np

from src.infra import DataReader


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


if __name__ == "__main__":
    INPUT_DATA = DataReader.read_txt("day3.txt", str)

    SINGLE_SLOPE = np.array((3, 1))
    RESULT = count_trees_hit(INPUT_DATA, np.array((0, 0)), SINGLE_SLOPE)
    print(f"With slope {(3, 1)} you hit {RESULT} trees.")

    RESULT_LIST = [RESULT]
    SLOPES = [
        np.array((1, 1)),
        np.array((5, 1)),
        np.array((7, 1)),
        np.array((1, 2))
    ]
    for SINGLE_SLOPE in SLOPES:
        RESULT = count_trees_hit(INPUT_DATA, np.array((0, 0)), SINGLE_SLOPE)
        RESULT_LIST.append(RESULT)
    RESULT_MULTI = np.prod(RESULT_LIST)
    print(f"\nWith multiple additional slopes, result is {RESULT_MULTI} trees.")
    print(f"Step results are: {RESULT_LIST}")
