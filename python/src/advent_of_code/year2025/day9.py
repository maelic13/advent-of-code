from itertools import combinations
from time import time_ns

from advent_of_code.infra import read_input, report_times


def day9() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 9, example=False).splitlines()
    red_tiles: list[tuple[int, int]] = []
    for line in inputs:
        x, y = line.split(",")
        red_tiles.append((int(x), int(y)))
    file_read_time = time_ns() - start

    # part 1
    max_area: int = 0
    for tile1, tile2 in combinations(red_tiles, 2):
        area = abs(tile1[0] - tile2[0] + 1) * abs(tile1[1] - tile2[1] + 1)
        max_area = max(max_area, area)
    print(max_area)
    part1_time = time_ns() - start

    # part 2
    part2_time = time_ns() - start

    # Report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day9()
