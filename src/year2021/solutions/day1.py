import numpy as np
from typing import List

from src.infra import DataReader


def count_increases(measurements: List[int]) -> int:
    increased = 0
    last_measurement = np.Inf
    for measurement in measurements:
        if measurement > last_measurement:
            increased += 1
        last_measurement = measurement
    return increased


if __name__ == "__main__":
    data = DataReader.read_txt("day1.txt", int)

    single_increases = count_increases(data)
    print(f"Measurement increased {single_increases} times in single mode.")

    sliding_window_sum: List[int] = list()
    for i in range(3, len(data) + 3):
        sliding_window_sum.append(sum(data[(i - 3):i]))

    sliding_window_increases = count_increases(sliding_window_sum)
    print(f"Measurement increased {sliding_window_increases} times in sliding window mode.")
