from time import time_ns

from advent_of_code.infra import read_input, report_times


def count_paths(
    current: str,
    end: str,
    missing_nodes: frozenset[str],
    devices: dict[str, list[str]],
    cache: dict[tuple[str, frozenset[str]], int],
) -> int:
    state = (current, missing_nodes)
    if state in cache:
        return cache[state]

    if current == end:
        return 1 if not missing_nodes else 0

    count = 0
    for node in devices[current]:
        new_missing = missing_nodes
        if node in missing_nodes:
            new_missing = missing_nodes - {node}

        count += count_paths(node, end, new_missing, devices, cache)

    cache[state] = count
    return count


def day11() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 11, example=False).splitlines()
    devices: dict[str, list[str]] = {}
    for device_str in inputs:
        device, outputs = device_str.split(": ")
        devices[device] = outputs.split(" ")
    file_read_time = time_ns() - start

    # part 1
    print(count_paths("you", "out", frozenset(), devices, {}))
    part1_time = time_ns() - start

    # part 2
    print(count_paths("svr", "out", frozenset(["dac", "fft"]), devices, {}))
    part2_time = time_ns() - start

    # Report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day11()
