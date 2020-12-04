import numpy as np

from src.infra.api import DataReader

from src.solutions.d3_t1 import TobogganRouteTracker


if __name__ == "__main__":
    input_data = DataReader.read_txt("d3_t1.txt", str)

    result = 1
    slopes = [
        np.array((1, 1)),
        np.array((3, 1)),
        np.array((5, 1)),
        np.array((7, 1)),
        np.array((1, 2))
    ]

    for slope in slopes:
        result *= TobogganRouteTracker(input_data).count_trees_hit(np.array((0, 0)), slope)
    print("Result is: {} trees.".format(result))
