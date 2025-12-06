from time import time_ns

from advent_of_code.infra import read_input, report_times


def max_power(batteries: str, battery_count: int) -> int:
    power_indices = []
    current_index = 0
    for i in range(battery_count - 1, -1, -1):
        index = find_max_power_index(batteries[current_index : len(batteries) - i])
        power_indices.append(index + current_index)
        current_index += index + 1
    return sum(
        int(x) * 10**i
        for i, x in enumerate(reversed([batteries[index] for index in power_indices]))
    )


def find_max_power_index(batteries: str) -> int:
    for i in "9876543210":
        try:
            return batteries.index(i)
        except ValueError:
            continue
    msg = "Could not find the maximum power index."
    raise ValueError(msg)


def day3() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 3, example=False).splitlines()
    file_read_time = time_ns() - start

    # part 1
    print(sum(max_power(bank, 2) for bank in inputs))
    part1_time = time_ns() - start

    # part 2
    print(sum(max_power(bank, 12) for bank in inputs))
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day3()
