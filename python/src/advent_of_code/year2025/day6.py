from itertools import starmap
from math import prod
from time import time_ns

from advent_of_code.infra import read_input, report_times


def classical_calculation(items: list[str], operator: str) -> int:
    return prod(map(int, items)) if operator == "*" else sum(map(int, items))


def cephalopod_calculation(number_str: list[list[str]], operator: str) -> int:
    numbers: list[int] = [int("".join(item)) for item in number_str[::-1]]
    return prod(numbers) if operator == "*" else sum(numbers)


def day6() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 6, example=False).splitlines()
    file_read_time = time_ns() - start

    # part 1
    parsed_input: list[list[str]] = [[] for _ in range(len([x for x in inputs[0].split(" ") if x]))]
    for line in inputs:
        for i, item in enumerate([x for x in line.split(" ") if x]):
            parsed_input[i].append(item)
    print(sum(classical_calculation(x[:-1], x[-1]) for x in parsed_input))
    part1_time = time_ns() - start

    # part 2
    cols = zip(*inputs, strict=False)
    to_calculate: list[tuple[list[list[str]], str]] = []
    buffer: list[list[str]] = []
    operator: str = ""
    for col in cols:
        if "*" in col or "+" in col:
            if buffer:
                to_calculate.append((buffer, operator))
            buffer = []
            operator = col[-1]
        if any(c != " " for c in col):
            buffer.append(list(col[:-1]))
    to_calculate.append((buffer, operator))

    print(sum(starmap(cephalopod_calculation, to_calculate)))
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day6()
