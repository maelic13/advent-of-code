from time import time_ns


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
    with open("inputs/2025/day4.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # part 1
    diagram: list[list[int]] = []
    for line in lines:
        row = [1 if x == "@" else 0 for x in line.strip()]
        row.insert(0, 0)
        row.append(0)
        diagram.append(row)
    diagram.insert(0, [0] * len(diagram[0]))
    diagram.append([0] * len(diagram[0]))
    can_be_removed = count_accessible_paper(diagram)

    # part 1
    print(can_be_removed)

    # part 2
    while True:
        can_be_removed_new = count_accessible_paper(diagram)
        if can_be_removed_new == 0:
            break
        can_be_removed += can_be_removed_new
    print(can_be_removed)



if __name__ == "__main__":
    start = time_ns()
    day4()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
