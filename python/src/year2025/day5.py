import operator
from time import time_ns

from infra import read_input, report_times


def count_fresh_ingredients(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    count = 0
    for ingredient in ingredients:
        for single_range in ranges:
            if single_range[0] <= ingredient <= single_range[1]:
                count += 1
                break
    return count


def count_available_fresh_ingredients(ranges: list[tuple[int, int]]) -> int:
    sorted_ranges = sorted(ranges, key=operator.itemgetter(0))

    merged: list[tuple[int, int]] = [sorted_ranges[0]]
    for current in sorted_ranges[1:]:
        last = merged[-1]
        if current[0] <= last[1] + 1:
            merged[-1] = (last[0], max(last[1], current[1]))
            continue
        merged.append(current)

    return sum(interval[1] + 1 - interval[0] for interval in merged)


def day5() -> None:
    start = time_ns()

    # read and parse file
    sections = read_input(2025, 5, example=False).split("\n\n")

    ranges: list[tuple[int, int]] = []
    for line in sections[0].splitlines():
        a, b = line.split("-")
        ranges.append((int(a), int(b)))
    ingredients = [int(line) for line in sections[1].splitlines()]
    file_read_time = time_ns() - start

    # part 1
    print(count_fresh_ingredients(ranges, ingredients))
    part1_time = time_ns() - start

    # part 2
    print(count_available_fresh_ingredients(ranges))
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day5()
