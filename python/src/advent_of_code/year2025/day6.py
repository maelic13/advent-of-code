from math import prod
from time import time_ns

from advent_of_code.infra import read_input, report_times


def perform_operations(items: list[str], operator: str) -> int:
    if operator == "+":
        return sum(map(int, items))
    return prod(map(int, items))


def perform_operations_cephalopod_numbers() -> None:
    pass


def day6() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 6, example=False).splitlines()

    parsed_input: list[list[str]] = [[] for _ in range(len([x for x in inputs[0].split(" ") if x]))]
    for line in inputs:
        for i, item in enumerate([x for x in line.split(" ") if x]):
            parsed_input[i].append(item)
    file_read_time = time_ns() - start

    # part 1
    print(sum(perform_operations(x[:-1], x[-1]) for x in parsed_input))
    part1_time = time_ns() - start

    # part 2
    print(perform_operations_cephalopod_numbers())
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day6()
