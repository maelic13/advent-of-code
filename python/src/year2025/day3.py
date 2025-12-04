from time import time_ns


def max_power(batteries: str, battery_count: int) -> int:
    power_indices = []
    current_index = 0
    for i in range(battery_count - 1, -1, -1):
        index = find_max_power_index(
            batteries[current_index : len(batteries) - i]
        )
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
    raise ValueError("Could not find the maximum power index.")


def day3() -> None:
    with open("inputs/2025/day3.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # part 1
    print(sum(max_power(bank.strip(), 2) for bank in lines))

    # part 2
    print(sum(max_power(bank.strip(), 12) for bank in lines))


if __name__ == "__main__":
    start = time_ns()
    day3()
    print(f"Execution time: {round((time_ns() - start) / 1000000, 1)} milliseconds.")
