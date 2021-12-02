from typing import List, Tuple

from src.year2020.infra.api import DataReader


def calculate_position(course: List[str], initial_position: Tuple[int, int] = (0, 0)
                       ) -> Tuple[int, int]:
    distance, depth = initial_position
    for instruction in course:
        command, value = instruction.split(" ")
        if command == "forward":
            distance += int(value)
        elif command == "down":
            depth += int(value)
        elif command == "up":
            depth -= int(value)
    return distance, depth


def calculate_position_with_aim(course: List[str],
                                initial_position: Tuple[int, int, int] = (0, 0, 0)
                                ) -> Tuple[int, int]:
    aim, distance, depth = initial_position
    for instruction in course:
        command, value = instruction.split(" ")
        if command == "forward":
            distance += int(value)
            depth += aim * int(value)
        elif command == "down":
            aim += int(value)
        elif command == "up":
            aim -= int(value)
    return distance, depth


if __name__ == "__main__":
    data = DataReader.read_txt("day2.txt", str)
    hor, dep = calculate_position(data)
    print(f"Multiplied horizontal and vertical positions: {hor * dep}.")

    hor2, dep2 = calculate_position_with_aim(data)
    print(f"Multiplied horizontal and vertical positions: {hor2 * dep2} with aim.")
