from multiprocessing import Pool
from string import ascii_lowercase

import numpy as np


class Map:
    def __init__(self, grid_2d: list[list[int]], start: tuple[int, ...],
                 goal: tuple[int, ...]) -> None:
        self.map = grid_2d
        self.start = start
        self.goal = goal

    def find_path(self) -> tuple[list[tuple[int, ...]], float]:
        open_set = {self.start}
        came_from: dict[tuple[int, ...], tuple[int, ...]] = {}
        g_score: dict[tuple[int, ...], float] = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.goal)}

        while open_set:
            current = min(open_set, key=lambda x: f_score[x])
            if current == self.goal:
                return self.reconstruct_path(came_from, current), f_score[current]

            open_set.remove(current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score.get(current, float("inf")) + 1
                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return [], float("inf")

    def get_neighbors(self, original_position: tuple[int, ...]) -> list[tuple[int, ...]]:
        possible_moves: list[np.ndarray] = []
        position = np.array(original_position)
        # up
        if (not position[0] - 1 < 0 and not self.map[position[0] - 1][position[1]]
                - self.map[position[0]][position[1]] > 1):
            possible_moves.append(np.array((position[0] - 1, position[1])) - position)
        # down
        if (not position[0] + 1 > len(self.map) - 1 and not self.map[position[0] + 1][position[1]]
                - self.map[position[0]][position[1]] > 1):
            possible_moves.append(np.array((position[0] + 1, position[1])) - position)
        # left
        if (not position[1] - 1 < 0 and not self.map[position[0]][position[1] - 1]
                - self.map[position[0]][position[1]] > 1):
            possible_moves.append(np.array((position[0], position[1] - 1)) - position)
        # right
        if (not position[1] + 1 > len(self.map[0]) - 1
                and not self.map[position[0]][position[1] + 1]
                - self.map[position[0]][position[1]] > 1):
            possible_moves.append(np.array((position[0], position[1] + 1)) - position)
        return [tuple(position + x) for x in possible_moves]

    @staticmethod
    def heuristic(position: tuple[int, ...], goal: tuple[int, ...]) -> float:
        return sum(goal) - sum(position)

    @staticmethod
    def reconstruct_path(came_from: dict[tuple[int, ...], tuple[int, ...]], current: tuple[int, ...]
                         ) -> list[tuple[int, ...]]:
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return list(reversed(total_path))


def finder(area_map: Map) -> tuple[list[tuple[int, ...]], float]:
    return area_map.find_path()


def find_shortest_path(grid: list[list[int]], start_points: list[tuple[int, ...]],
                       end_point: tuple[int, ...]) -> tuple[list[tuple[int, ...]], float]:
    maps = [Map(grid, start_point, end_point) for start_point in start_points]
    with Pool() as pool:
        results = pool.map(finder, maps)
        pool.close()
        pool.join()
    best_path, steps = min(results, key=lambda x: x[1])
    return best_path, steps


def parse_map_data(map_data: list[str]) -> tuple[list[list[int]], tuple[int, ...], tuple[int, ...]]:
    grid: list[list[int]] = []
    start: tuple[int, ...] = (0, 0)
    goal: tuple[int, ...] = (0, 0)
    for y_coord, line in enumerate(map_data):
        x_grid: list[int] = []
        for x_coord, height in enumerate(line.strip()):
            if height == "S":
                start = (y_coord, x_coord)
                x_grid.append(ascii_lowercase.index("a"))
                continue
            if height == "E":
                goal = (y_coord, x_coord)
                x_grid.append(ascii_lowercase.index("z"))
                continue
            x_grid.append(ascii_lowercase.index(height))
        grid.append(x_grid)
    return grid, start, goal


def advent12() -> None:
    with open("inputs/2022/day12.txt", "r") as file:
        lines = file.readlines()

    grid, start, goal = parse_map_data(lines)

    # part 1
    path, steps = find_shortest_path(grid, [start], goal)
    print(path)
    print(steps)

    # part 2
    start_points: list[tuple[int, ...]] = []
    for y_coord, x_grid in enumerate(grid):
        for x_coord, height in enumerate(x_grid):
            if height == 0:
                start_points.append((y_coord, x_coord))

    path, steps = find_shortest_path(grid, start_points, goal)
    print(path)
    print(steps)


if __name__ == "__main__":
    advent12()
