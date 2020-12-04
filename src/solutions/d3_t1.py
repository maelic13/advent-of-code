from copy import copy
from math import gcd
import numpy as np
from typing import List

from src.infra.api import DataReader


class TobogganRouteTracker:
    def __init__(self, tree_map: List) -> None:
        self._map = tree_map

    def count_trees_hit(self, current_pos: np.ndarray, slope: np.ndarray) -> int:
        slope = slope / gcd(slope[0], slope[1])
        trees_hit = 0
        while current_pos[1] < len(self._map):
            x = int(current_pos[1])
            y = int(current_pos[0]) % len(self._map[x])
            if self._map[x][y] == "#":
                trees_hit += 1
            current_pos = np.add(current_pos, slope)
        return trees_hit


if __name__ == "__main__":
    input_data = DataReader.read_txt("d3_t1.txt", str)
    result = TobogganRouteTracker(input_data).count_trees_hit(np.array((0, 0)), np.array((3, 1)))
    print("You hit {} trees.".format(result))
