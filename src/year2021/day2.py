from src.infra import DataReader


def calculate_position(course: list[str], initial_position: tuple[int, int] = (0, 0)
                       ) -> tuple[int, int]:
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


def calculate_position_with_aim(course: list[str],
                                initial_position: tuple[int, int, int] = (0, 0, 0)
                                ) -> tuple[int, int]:
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


def advent2() -> None:
    data = DataReader.read_txt("day2.txt", str)
    hor, dep = calculate_position(data)
    print(f"Multiplied horizontal and vertical positions: {hor * dep}.")

    hor2, dep2 = calculate_position_with_aim(data)
    print(f"Multiplied horizontal and vertical positions: {hor2 * dep2} with aim.")


if __name__ == "__main__":
    advent2()
