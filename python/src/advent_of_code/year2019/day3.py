from copy import copy


class Wire:
    def __init__(self, wire: list[str], beginning: list[int]) -> None:
        self._wire = wire
        self._beginning = beginning
        self.wire_locations: list[tuple[int, int]] = self._calculate_wire_locations()

    def _calculate_wire_locations(self) -> list[tuple[int, int]]:
        if not self._wire:
            msg = "No data for wire!"
            raise RuntimeError(msg)

        current_location = copy(self._beginning)
        locations: list[tuple[int, int]] = []

        for direction in self._wire:
            command = direction[0]
            steps = int(direction[1:])

            if command == "R":
                locations.extend(
                    (current_location[0], current_location[1] + (i + 1)) for i in range(steps)
                )
                current_location[1] += steps
            elif command == "L":
                locations.extend(
                    (current_location[0], current_location[1] - (i + 1)) for i in range(steps)
                )
                current_location[1] -= steps
            elif command == "U":
                locations.extend(
                    (current_location[0] + (i + 1), current_location[1]) for i in range(steps)
                )
                current_location[0] += steps
            elif command == "D":
                locations.extend(
                    (current_location[0] - (i + 1), current_location[1]) for i in range(steps)
                )
                current_location[0] -= steps
            else:
                msg = "Incorrect command!"
                raise ValueError(msg)
        return locations

    def get_number_of_steps(self, intersection: tuple[int, int]) -> int:
        return self.wire_locations.index(intersection) + 1


class FrontPanel:
    def __init__(self, wire_1: Wire, wire_2: Wire) -> None:
        self.intersections: list[tuple[int, int]] = []
        self.closest_intersection: tuple[int, int] | None = None
        self.dist_to_closest: float | None = None
        self.quickest_intersection: tuple[int, int] | None = None
        self.fewest_steps: int | None = None
        self._wire1: Wire = wire_1
        self._wire2: Wire = wire_2

    @staticmethod
    def from_file(input_file: str) -> FrontPanel:
        with open(input_file, encoding="utf-8") as file:
            return FrontPanel(
                Wire(file.readline().split(","), [0, 0]), Wire(file.readline().split(","), [0, 0])
            )

    def calculate_intersections(self) -> None:
        locations1 = self._wire1.wire_locations
        locations2 = self._wire2.wire_locations
        intersections = set(locations1) & set(locations2)
        self.intersections = list(intersections)

    def calculate_closest_intersection(self) -> None:
        min_distance = float("inf")
        closest_intersection = None
        for intersection in self.intersections:
            distance = abs(intersection[0]) + abs(intersection[1])
            if distance < min_distance:
                min_distance = distance
                closest_intersection = intersection
        self.dist_to_closest = min_distance
        self.closest_intersection = closest_intersection

    def calculate_quickest_intersection(self) -> None:
        if not self.intersections:
            self.calculate_intersections()

        fewest_steps = float("inf")
        for intersection in self.intersections:
            steps1 = self._wire1.get_number_of_steps(intersection)
            steps2 = self._wire2.get_number_of_steps(intersection)
            if (steps1 + steps2) < fewest_steps:
                fewest_steps = steps1 + steps2
                self.quickest_intersection = intersection
                self.fewest_steps = fewest_steps


def advent3() -> None:
    input_file = "inputs/2019/day3.txt"
    panel = FrontPanel.from_file(input_file)

    panel.calculate_intersections()
    panel.calculate_closest_intersection()
    panel.calculate_quickest_intersection()

    print(
        f"Intersections found: {len(panel.intersections)}\n"
        f"Closest intersection: {panel.closest_intersection}\n"
        f"Distance to closest intersection: {panel.dist_to_closest}\n"
        f"Quickest intersection: {panel.quickest_intersection}\n"
        f"Fewest steps to intersection: {panel.fewest_steps}\n"
    )


if __name__ == "__main__":
    advent3()
