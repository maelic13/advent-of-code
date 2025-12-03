from time import time_ns


def calculate_move(command: str) -> int:
    if command[0] == "R":
        return int(command[1:])
    return -int(command[1:])


def day1() -> None:
    with open("inputs/2025/day1.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # part 1
    current_position = 50
    password_1 = 0
    for line in lines:
        current_position = (current_position + calculate_move(line.strip())) % 100
        if current_position == 0:
            password_1 += 1
    print(password_1)

    # part 2
    current_position = 50
    password_2 = 0
    for line in lines:
        for _ in range(int(line.strip()[1:])):
            if line[0] == "R":
                current_position += 1
            else:
                current_position -= 1
            current_position %= 100
            if current_position == 0:
                password_2 += 1
    print(password_2)


if __name__ == "__main__":
    start = time_ns()
    day1()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
