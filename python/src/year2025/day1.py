from time import time_ns

from infra import read_input, report_times


def calculate_move(command: str) -> int:
    if command[0] == "R":
        return int(command[1:])
    return -int(command[1:])


def day1() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 1, example=False).splitlines()
    file_read_time = time_ns() - start

    # part 1
    current_position = 50
    password_1 = 0
    for line in inputs:
        current_position = (current_position + calculate_move(line)) % 100
        if current_position == 0:
            password_1 += 1
    print(password_1)
    part1_time = time_ns() - start

    # part 2
    current_position = 50
    password_2 = 0
    for line in inputs:
        for _ in range(int(line[1:])):
            if line[0] == "R":
                current_position += 1
            else:
                current_position -= 1
            current_position %= 100
            if current_position == 0:
                password_2 += 1
    print(password_2)
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day1()
