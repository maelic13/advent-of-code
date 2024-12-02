from time import time_ns


def day1() -> None:
    with open("inputs/2024/day1.txt", "r") as file:
        lines = file.readlines()

    firsts: list[int] = []
    seconds: list[int] = []
    for line in lines:
        first, second = line.strip().split()
        firsts.append(int(first))
        seconds.append(int(second))

    # part 1
    print(sum(abs(first - second) for first, second in zip(sorted(firsts), sorted(seconds))))

    # part 2
    print(sum(first * seconds.count(first) for first in firsts))


if __name__ == "__main__":
    start = time_ns()
    day1()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
