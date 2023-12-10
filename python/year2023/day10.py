from time import time

import numpy as np


class FieldMap:
    map_signs = {
        "|": (np.array((1, 0)), np.array((-1, 0))),
        "-": (np.array((0, 1)), np.array((0, -1))),
        "F": (np.array((1, 0)), np.array((0, 1))),
        "L": (np.array((-1, 0)), np.array((0, 1))),
        "J": (np.array((-1, 0)), np.array((0, -1))),
        "7": (np.array((1, 0)), np.array((0, -1))),
    }

    def __init__(self, field_map: list[str]) -> None:
        self._field = field_map
        self._loop_start = self._find_loop_start()

    def distance_to_furthest_point_from_start(self) -> int:
        steps_around_loop = len(self._find_loop_nodes())
        return int(steps_around_loop / 2) + steps_around_loop % 2

    def count_tiles_inside_loop(self) -> int:
        loop_nodes: list[tuple[int, int]] = [tuple(node) for node in self._find_loop_nodes()]
        tiles_count = 0

        for i, row in enumerate(self._field):
            for j, sign in enumerate(row):
                if self._is_in_loop(i, j, loop_nodes):
                    tiles_count += 1

        return tiles_count

    def _is_in_loop(self, x: int, y: int, loop_nodes: list[tuple[int, int]]) -> bool:
        crosses_x = [(i, y) for i in range(x)
                     if (i, y) in loop_nodes and self._field[i][y] in ("-", "L", "F", "7", "J")]
        if not len(crosses_x) % 2 == 1:
            return False
        crosses_y = [(x, i) for i in range(y)
                     if (x, i) in loop_nodes and self._field[x][i] in ("|", "L", "F", "7", "J")]
        return len(crosses_y) % 2 == 1 and (x, y) not in loop_nodes

    def _find_loop_nodes(self) -> list[np.ndarray]:
        previous_position = self._loop_start.copy()
        current_position = self._find_connections(self._loop_start)[0]
        loop_nodes: list[np.ndarray] = [self._loop_start.copy()]

        while not np.all(current_position == self._loop_start):
            for direction in self.map_signs[self._field[current_position[0]][current_position[1]]]:
                if np.all(current_position + direction == previous_position):
                    continue
                previous_position = current_position.copy()
                current_position += direction
                loop_nodes.append(current_position.copy())
                break

        return loop_nodes

    def _find_loop_start(self) -> np.ndarray:
        for i, row in enumerate(self._field):
            for j, sign in enumerate(row):
                if sign == "S":
                    return np.array((i, j))
        raise RuntimeError("Could not find starting position.")

    def _find_connections(self, position: np.ndarray) -> list[np.ndarray]:
        connections: list[np.ndarray] = []

        up = position + np.array((-1, 0))
        down = position + np.array((1, 0))
        left = position + np.array((0, -1))
        right = position + np.array((0, 1))

        if self._field[up[0]][up[1]] in ("|", "7", "F"):
            connections.append(up)
        if self._field[down[0]][down[1]] in ("|", "J", "L"):
            connections.append(down)
        if self._field[left[0]][left[1]] in ("-", "F", "L"):
            connections.append(left)
        if self._field[right[0]][right[1]] in ("-", "7", "J"):
            connections.append(right)

        return connections


def day10() -> None:
    with open("inputs/2023/day10.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]
    field_map = FieldMap(lines)

    # part 1
    print(field_map.distance_to_furthest_point_from_start())

    # part 2
    print(field_map.count_tiles_inside_loop())


if __name__ == "__main__":
    start = time()
    day10()
    print(f"Execution time: {round(time() - start)} seconds.")
