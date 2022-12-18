from typing import Optional

import numpy as np


class Cave:
    def __init__(self, rocks: set[tuple[int, ...]], ground_level: bool = False) -> None:
        self.finished = False
        self.ground_level: Optional[int] = max(x[1] for x in rocks) + 2 if ground_level else None
        self.intersections: list[tuple[int, ...]] = []
        self.rocks = rocks
        self.sand: set[tuple[int, ...]] = set()
        self.sand_entry_point = (500, 0)

    def __repr__(self) -> str:
        x_min = min(x[0] for x in self.rocks.union(self.sand))
        x_max = max(x[0] for x in self.rocks.union(self.sand))
        y_max = max(x[1] for x in self.rocks.union(self.sand))

        representation = ""
        for y_coord in range(self.ground_level + 1 if self.ground_level else y_max + 1):
            for x_coord in range(x_min, x_max + 1):
                if (x_coord, y_coord) in self.rocks or y_coord == self.ground_level:
                    representation += " # "
                elif (x_coord, y_coord) in self.sand:
                    representation += " o "
                elif (x_coord, y_coord) == self.sand_entry_point:
                    representation += " + "
                else:
                    representation += " . "
            representation += "\n"
        return representation

    @property
    def resting_sand(self) -> int:
        return len(self.sand)

    @classmethod
    def from_txt(cls, input_lines: list[str]) -> "Cave":
        commands: list[list[np.ndarray]] = []
        for line in input_lines:
            command_row: list[np.ndarray] = []
            for command in line.strip().split(" -> "):
                x_coord, y_coord = command.split(",")
                command_row.append(np.array((int(x_coord), int(y_coord))))
            commands.append(command_row)

        rocks: set[tuple[int, ...]] = set()
        for formation_commands in commands:
            for i in range(len(formation_commands) - 1):
                for node in cls.nodes_in_between(formation_commands[i], formation_commands[i + 1]):
                    rocks.add(tuple(node))
        return Cave(rocks)

    def reset(self) -> None:
        self.finished = False
        self.ground_level = None
        self.sand = set()

    def activate_ground(self) -> None:
        self.ground_level = max(x[1] for x in self.rocks) + 2

    @staticmethod
    def nodes_in_between(node1: np.ndarray, node2: np.ndarray) -> list[np.ndarray]:
        vector = node2 - node1
        distance = abs(sum(vector))
        step = vector // distance

        result_nodes: list[np.ndarray] = [node1]
        for i in range(distance):
            result_nodes.append(result_nodes[i] + step)
        return result_nodes

    def drop_sand(self) -> bool:
        if self.finished:
            return False

        position = (np.array(self.intersections[-1])
                    if self.intersections else np.array(self.sand_entry_point))
        while True:
            position = self.drop_down(position)  # type: ignore
            if position is None:
                return False
            if tuple(position) not in self.intersections:
                self.intersections.append(tuple(position))
            for step in [np.array((-1, 1)), np.array((1, 1))]:
                if (tuple(position + step) in self.rocks.union(self.sand)
                        or (position + step)[1] == self.ground_level):
                    new_position = position
                    continue
                new_position = position + step
                break
            if np.all(new_position == position):
                if tuple(position) == self.sand_entry_point:
                    self.finished = True
                self.intersections.remove(tuple(new_position))
                break
            position = new_position
        self.sand.add(tuple(position))
        return True

    def drop_down(self, position: np.ndarray) -> Optional[np.ndarray]:
        blockers_downward = sorted((np.array(x) for x in self.rocks.union(self.sand)
                                    if x[0] == position[0] and x[1] > position[1]),
                                   key=lambda x: x[1])
        if not blockers_downward and not self.ground_level:
            self.finished = True
            return None
        if not blockers_downward and self.ground_level:
            return np.array((position[0], self.ground_level - 1))
        return blockers_downward[0] + np.array((0, -1))


def advent14() -> None:
    with open("../inputs/day14.txt", "r") as file:
        lines = file.readlines()
    cave = Cave.from_txt(lines)

    # part 1
    while not cave.finished:
        cave.drop_sand()
    print(cave)
    print(cave.finished)
    print(cave.resting_sand)

    # part 2
    cave.reset()
    cave.activate_ground()
    while not cave.finished:
        cave.drop_sand()
    print(cave)
    print(cave.finished)
    print(cave.resting_sand)


if __name__ == "__main__":
    advent14()
