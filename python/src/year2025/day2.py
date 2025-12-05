from time import time_ns

from regex import findall

from infra import read_input, report_times


def is_id_invalid(i: int) -> bool:
    id_string = str(i)
    if len(id_string) % 2 != 0:
        return False

    return id_string[: len(id_string) // 2] == id_string[len(id_string) // 2 :]


def is_id_invalid_2(number: int) -> bool:
    id_string = str(number)
    match = findall(r"^(.+)\1+$", id_string)
    return bool(match)


def day2() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 2, example=False).strip().split(",")

    invalid_ids: set[int] = set()
    for string in inputs:
        begin, end = string.split("-")
        for i in range(int(begin), int(end) + 1):
            if i in invalid_ids:
                continue
            if is_id_invalid(i):
                invalid_ids.add(i)
    file_read_time = time_ns() - start

    # part 1
    print(sum(invalid_ids))
    part1_time = time_ns() - start

    # part 2
    invalid_ids: set[int] = set()
    for string in inputs:
        begin, end = string.split("-")
        for i in range(int(begin), int(end) + 1):
            if i in invalid_ids:
                continue
            if is_id_invalid_2(i):
                invalid_ids.add(i)
    print(sum(invalid_ids))
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day2()
