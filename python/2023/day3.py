from time import time_ns
from re import finditer, Match

import numpy as np


class Gear:
    def __init__(self, position: tuple[int, int], part_numbers: list[int]) -> None:
        self.position = position
        self.part_numbers = part_numbers

    def __repr__(self) -> str:
        return f"Gear at {self.position} with part numbers {self.part_numbers}"

    def num_parts(self) -> int:
        return len(self.part_numbers)

    def gear_ratio(self) -> int:
        return np.prod(self.part_numbers)


class EngineSchematic:
    def __init__(self, schematic: list[str]) -> None:
        self.schematic = schematic

    def find_part_numbers(self) -> list[int]:
        part_numbers = []

        for line_number, line in enumerate(self.schematic):
            for number in finditer(r"\d+", line):
                if self.is_part_number(number, line_number):
                    part_numbers.append(int(number.group()))

        return part_numbers

    def is_part_number(self, number: Match[str], line_number: int) -> bool:
        left_border = max(number.start() - 1, 0)
        right_border = min(number.end() + 1, len(self.schematic[0]) - 1)
        up_border = max(line_number - 1, 0)
        down_border = min(line_number + 1, len(self.schematic) - 1)

        for line_num in range(up_border, down_border + 1):
            for char in self.schematic[line_num][left_border:right_border]:
                if not char.isdigit() and char != ".":
                    return True
        return False

    def find_gears(self) -> list[Gear]:
        gears: list[Gear] = []

        for line_number, line in enumerate(self.schematic):
            for gear in finditer(r"\*", line):
                gears.append(self.create_gear(gear, line_number))

        return gears

    def create_gear(self, gear: Match[str], line_number: int) -> Gear:
        up_border = max(line_number - 1, 0)
        down_border = min(line_number + 1, len(self.schematic) - 1)

        part_numbers = []
        for line_num in range(up_border, down_border + 1):
            for number in finditer(r"\d+", self.schematic[line_num]):
                if gear.start() in range(number.start() - 1, number.end() + 1):
                    part_numbers.append(int(number.group()))

        return Gear((gear.start(), line_number), part_numbers)


def day3() -> None:
    with open("inputs/2023/day3.txt", "r") as file:
        lines = file.readlines()

    schematic = EngineSchematic(lines)

    # part 1
    print(sum(schematic.find_part_numbers()))
    # part 2
    print(sum(gear.gear_ratio() for gear in schematic.find_gears() if gear.num_parts() == 2))


if __name__ == "__main__":
    start = time_ns()
    day3()
    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
