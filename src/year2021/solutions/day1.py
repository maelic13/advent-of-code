from src.infra import DataReader


def count_increases(measurements: list[int]) -> int:
    increased = 0
    last_measurement = float("inf")
    for measurement in measurements:
        if measurement > last_measurement:
            increased += 1
        last_measurement = measurement
    return increased


if __name__ == "__main__":
    data = DataReader.read_txt("day1.txt", int)

    SINGLE_INCREASES = count_increases(data)
    print(f"Measurement increased {SINGLE_INCREASES} times in single mode.")

    sliding_window_sum: list[int] = []
    for i in range(3, len(data) + 3):
        sliding_window_sum.append(sum(data[(i - 3):i]))

    SLIDING_WINDOW_INCREASES = count_increases(sliding_window_sum)
    print(f"Measurement increased {SLIDING_WINDOW_INCREASES} times in sliding window mode.")
