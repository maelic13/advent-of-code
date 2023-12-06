import numpy as np


class Knot:
    def __init__(self, start_position: np.ndarray = np.array((0, 0))) -> None:
        self.position = start_position.copy()
        self.visited: set[tuple[int, ...]] = {tuple(start_position.copy())}

    def add_current(self) -> None:
        self.visited.add(tuple(self.position.copy()))


class Simulation:
    def __init__(self, knots: list[Knot]) -> None:
        self.knots = knots

    @property
    def head(self) -> Knot:
        return self.knots[0]

    @property
    def tail_visited(self) -> set[tuple[int, ...]]:
        return self.knots[-1].visited

    @staticmethod
    def vector(direction: str) -> np.ndarray:
        direction_vectors = {
            "U": np.array((0, 1)),
            "D": np.array((0, -1)),
            "L": np.array((-1, 0)),
            "R": np.array((1, 0))
        }
        return direction_vectors[direction]

    def make_move(self, direction: str, distance: int) -> None:
        vector = self.vector(direction)

        for _ in range(distance):
            self.head.position += vector
            self.head.add_current()

            for i, knot in enumerate(self.knots[1:], 1):
                knot.position += self._tail_vector(self.knots[i - 1].position, knot.position)
                knot.add_current()

    @staticmethod
    def _tail_vector(head: np.ndarray, tail: np.ndarray) -> np.ndarray:
        vector = head - tail
        if np.linalg.norm(vector) < 2:
            return np.array((0, 0))
        return np.sign(vector)


def advent9() -> None:
    with open("inputs/2022/day9.txt", "r") as file:
        lines = file.readlines()

    # part 1
    sim = Simulation([Knot() for _ in range(2)])
    for line in lines:
        direction, distance = line.strip().split()
        sim.make_move(direction, int(distance))
    print(len(sim.tail_visited))

    # part 2
    sim = Simulation([Knot() for _ in range(10)])
    for line in lines:
        direction, distance = line.strip().split()
        sim.make_move(direction, int(distance))
    print(len(sim.tail_visited))


if __name__ == "__main__":
    advent9()
