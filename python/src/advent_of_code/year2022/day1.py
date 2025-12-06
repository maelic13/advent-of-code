from time import time_ns

if __name__ == "__main__":
    start = time_ns()

    with open("inputs/2022/day1.txt", encoding="utf-8") as file:
        lines = file.readlines()

    sums: list[int] = []
    BUFF = 0
    for line in lines:
        if line == "\n":
            sums.append(BUFF)
            BUFF = 0
            continue
        BUFF += int(line.strip())

    # part 1
    print(max(sums))

    # part 2
    print(sum(sorted(sums)[-3:]))

    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
