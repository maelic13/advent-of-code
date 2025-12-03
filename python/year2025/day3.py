from time import time_ns


class BankBattery:
    def __init__(self, batteries: tuple[int, ...]) -> None:
        self.batteries = batteries

    def max_power(self, battery_count: int) -> int:
        power_indices = []
        current_index = 0
        for i in range(battery_count - 1, -1, -1):
            index = self._find_max_power_index(self.batteries[current_index:len(self.batteries) - i])
            power_indices.append(index + current_index)
            current_index += index + 1
        return sum(x * 10 ** i for i, x in enumerate(reversed([self.batteries[index] for index in power_indices])))

    @staticmethod
    def _find_max_power_index(batteries: tuple[int, ...]) -> int:
        for i in range(9, -1, -1):
            try:
                return batteries.index(i)
            except ValueError:
                continue
        raise ValueError


def day3() -> None:
    with open("inputs/2025/day3.txt", "r") as file:
        lines = file.readlines()

    # part 1
    banks: list[BankBattery] = []
    for line in lines:
        banks.append(BankBattery(tuple(int(x) for x in line.strip())))
    print(sum(bank.max_power(2) for bank in banks))

    # part 2
    print(sum(bank.max_power(12) for bank in banks))


if __name__ == "__main__":
    start = time_ns()
    day3()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
