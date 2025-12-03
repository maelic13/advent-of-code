from time import time_ns


def count_increases(measurements: list[int]) -> int:
    increased = 0
    last_measurement = float("inf")
    for measurement in measurements:
        if measurement > last_measurement:
            increased += 1
        last_measurement = measurement
    return increased


def advent1() -> None:
    with open("inputs/2021/day1.txt", encoding="utf-8") as file:
        data = [int(line.strip()) for line in file]

    single_increases = count_increases(data)
    print(f"Measurement increased {single_increases} times in single mode.")

    sliding_window_sum: list[int] = [sum(data[(i - 3) : i]) for i in range(3, len(data) + 3)]

    sliding_window_increases = count_increases(sliding_window_sum)
    print(f"Measurement increased {sliding_window_increases} times in sliding window mode.")


if __name__ == "__main__":
    start = time_ns()
    advent1()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
