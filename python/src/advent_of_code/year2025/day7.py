from copy import copy
from time import time_ns

from advent_of_code.infra import read_input, report_times


def expand_node(node: tuple[int, int], space: list[str]) -> list[tuple[int, int]]:
    if space[node[0]][node[1]] != "^":
        return [(node[0] + 1, node[1])]

    return [(node[0] + 1, node[1] + 1), (node[0] + 1, node[1] - 1)]


def count_splits(space: list[str]) -> int:
    beams: set[int] = {space[0].index("S")}
    splits: int = 0
    for line in space[1:]:
        for index in copy(beams):
            if line[index] == "^":
                splits += 1
                beams.remove(index)
                beams.add(index + 1)
                beams.add(index - 1)
    return splits


def count_realities(
    beam_position: tuple[int, int],
    space: list[str],
    cache: dict[tuple[int, int], int],
) -> int:
    if beam_position in cache:
        return cache[beam_position]

    if beam_position[0] >= len(space):
        cache[beam_position] = 1
        return 1

    count = 0
    for node in expand_node(beam_position, space):
        count += count_realities(node, space, cache)
    cache[beam_position] = count
    return count


def day6() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 7, example=False).splitlines()
    file_read_time = time_ns() - start

    # part 1
    print(count_splits(inputs))
    part1_time = time_ns() - start

    # part 2
    print(count_realities((0, inputs[0].index("S")), inputs, {}))
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day6()
