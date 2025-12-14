from itertools import combinations, pairwise, starmap
from time import time_ns

from advent_of_code.infra import read_input, report_times

type Point2D = tuple[int, int]


def find_max_area(red_tiles: list[Point2D]) -> int:
    edges: list[tuple[Point2D, Point2D]] = get_edges(red_tiles)
    max_area = 0

    for tile1, tile2 in combinations(red_tiles, 2):
        area = calculate_area(tile1, tile2)

        if area <= max_area:
            continue

        if not area_intersected(tile1, tile2, edges):
            max_area = area

    return max_area


def get_edges(red_tiles: list[Point2D]) -> list[tuple[Point2D, Point2D]]:
    edges: list[tuple[Point2D, Point2D]] = [(red_tiles[0], red_tiles[-1])]
    for tile1, tile2 in pairwise(red_tiles):
        edges.append((tile1, tile2))
    return edges


def calculate_area(tile1: Point2D, tile2: Point2D) -> int:
    return (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)


def area_intersected(tile1: Point2D, tile2: Point2D, edges: list[tuple[Point2D, Point2D]]) -> bool:
    area_x_min, area_x_max = sorted((tile1[0], tile2[0]))
    area_y_min, area_y_max = sorted((tile1[1], tile2[1]))

    for (edge1_x, edge1_y), (edge2_x, edge2_y) in edges:
        if edge1_x == edge2_x:
            if area_x_min < edge1_x < area_x_max:
                edge_y_min, edge_y_max = min(edge1_y, edge2_y), max(edge1_y, edge2_y)
                if max(area_y_min, edge_y_min) < min(area_y_max, edge_y_max):
                    return True
            continue

        if area_y_min < edge1_y < area_y_max:
            edge_x_min, edge_x_max = min(edge1_x, edge2_x), max(edge1_x, edge2_x)
            if max(area_x_min, edge_x_min) < min(area_x_max, edge_x_max):
                return True

    return False


def day9() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 9, example=False).splitlines()
    red_tiles: list[Point2D] = []
    for line in inputs:
        x, y = line.split(",")
        red_tiles.append((int(x), int(y)))
    file_read_time = time_ns() - start

    # part 1
    print(max(starmap(calculate_area, combinations(red_tiles, 2))))
    part1_time = time_ns() - start

    # part 2
    print(find_max_area(red_tiles))
    part2_time = time_ns() - start

    # Report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day9()
