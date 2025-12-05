from time import time_ns

from infra import read_input, report_times


def count_accessible_paper(diagram: list[list[int]]) -> int:
    accessible: list[tuple[int, int]] = []
    for row in range(1, len(diagram) - 1):
        for col in range(1, len(diagram[row]) - 1):
            if diagram[row][col] == 0:
                continue
            if sum(diagram[row + i][col + j] for i in range(-1, 2) for j in range(-1, 2)) < 5:
                accessible.append((row, col))

    for row, col in accessible:
        diagram[row][col] = 0
    return len(accessible)


def day4() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 4, example=False).splitlines()

    diagram: list[list[int]] = []
    for line in inputs:
        row = [1 if x == "@" else 0 for x in line]
        row.insert(0, 0)
        row.append(0)
        diagram.append(row)
    diagram.insert(0, [0] * len(diagram[0]))
    diagram.append([0] * len(diagram[0]))
    can_be_removed = count_accessible_paper(diagram)
    file_read_time = time_ns() - start

    # part 1
    print(can_be_removed)
    part1_time = time_ns() - start

    # part 2
    while True:
        can_be_removed_new = count_accessible_paper(diagram)
        if can_be_removed_new == 0:
            break
        can_be_removed += can_be_removed_new
    print(can_be_removed)
    part2_time = time_ns() - start

    # report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day4()
