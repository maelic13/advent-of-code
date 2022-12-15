from multiprocessing import Pool
from typing import Iterable, Optional


import numpy as np


class Sensor:
    def __init__(self, position: tuple[int, int], nearest_beacon: tuple[int, int]) -> None:
        self.position = position
        self.beacon = nearest_beacon
        self.beacon_distance = self._distance(self.position, self.beacon)

    @property
    def min_x(self) -> int:
        return self.position[0] - self.beacon_distance

    @property
    def max_x(self) -> int:
        return self.position[0] + self.beacon_distance

    @property
    def min_y(self) -> int:
        return self.position[1] - self.beacon_distance

    @property
    def max_y(self) -> int:
        return self.position[1] + self.beacon_distance

    def guaranteed_empty(self, position: tuple[int, int]) -> bool:
        return (position != self.beacon and position != self.position
                and self._distance(self.position, position) <= self.beacon_distance)

    def in_y_range(self, y_coord: int) -> bool:
        return (self.position[1] - self.beacon_distance
                <= y_coord
                <= self.position[1] + self.beacon_distance)

    @staticmethod
    def _distance(position1: tuple[int, int], position2: tuple[int, int]) -> int:
        return sum(abs(x) for x in np.array(position1) - np.array(position2))


class AreaMap:
    def __init__(self, sensors: set[Sensor]) -> None:
        self.sensors = sensors
        self.empty: set[tuple[int, int]] = set()
        self.unknown: set[tuple[int, int]] = set()

    def __repr__(self) -> str:
        representation = ""
        for y_coord in range(self.min_y(), self.max_y() + 1):
            for x_coord in range(self.min_x(), self.max_x() + 1):
                if (x_coord, y_coord) in (x.beacon for x in self.sensors):
                    representation += " B "
                elif (x_coord, y_coord) in (x.position for x in self.sensors):
                    representation += " S "
                elif (x_coord, y_coord) in self.empty:
                    representation += " # "
                elif (x_coord, y_coord) in self.unknown:
                    representation += " : "
                else:
                    representation += " . "
            representation += "\n"
        return representation

    def min_x(self, sensors: Optional[Iterable[Sensor]] = None) -> int:
        if sensors is None:
            sensors = self.sensors
        return min(x.min_x for x in sensors)

    def max_x(self, sensors: Optional[Iterable[Sensor]] = None) -> int:
        if sensors is None:
            sensors = self.sensors
        return max(x.max_x for x in sensors)

    def min_y(self) -> int:
        return min(y.min_y for y in self.sensors)

    def max_y(self) -> int:
        return max(y.max_y for y in self.sensors)

    def add_position(self, position: tuple[int, int]) -> bool:
        """
        Add position to map.
        :param position: position to add
        :return: True if guaranteed empty, False if unknown or already evaluated
        """
        if (position in [x.position for x in self.sensors] + [x.beacon for x in self.sensors]
                or position in self.empty):
            return False

        for sensor in sorted(self.sensors, key=lambda x: abs(x.position[1] - position[1])):
            if sensor.guaranteed_empty(position):
                self.empty.add(position)
                return True
        self.unknown.add(position)
        return False

    def evaluate_section(self, x_limit: tuple[int, int] = (-np.inf, np.inf),
                         y_limit: tuple[int, int] = (-np.inf, np.inf)) -> None:
        for y_coord in range(y_limit[0], y_limit[1] + 1):
            sensors = [s for s in self.sensors if s.in_y_range(y_coord)]
            x_range = range(max(x_limit[0], self.min_x(sensors)),
                            min(x_limit[1], self.max_x(sensors) + 1))
            for unknown_position in ((x, y_coord) for x in x_range if
                                     x_limit[0] <= x <= x_limit[1]):
                self.add_position(unknown_position)

    def unknown_in_limits(self, x_limit: tuple[int, int] = (-np.inf, np.inf),
                          y_limit: tuple[int, int] = (-np.inf, np.inf)) -> list[tuple[int, int]]:
        return [u for u in self.unknown if x_limit[0] <= u[0] <= x_limit[1]
                and y_limit[0] <= u[1] <= y_limit[1]]

    def find_unknown(self, limit: int = np.inf) -> tuple[int, int]:
        to_check = {(x, y) for x in range(limit + 1) for y in range(limit + 1)}


def advent15() -> None:
    with open("inputs/day15.txt", "r") as file:
        lines = file.readlines()

    sensors: set[Sensor] = set()
    for line in lines:
        sensor_txt, beacon_txt = line.split("Sensor at x=")[1].split(": closest beacon is at x=")
        sensor_coord = sensor_txt.split(", y=")
        beacon_coord = beacon_txt.split(", y=")
        sensors.add(Sensor(position=(int(sensor_coord[0]), int(sensor_coord[1])),
                           nearest_beacon=(int(beacon_coord[0]), int(beacon_coord[1]))))
    area_map = AreaMap(sensors)

    # part 1
    # y_coord = 2000000
    # y_coord = 10
    # area_map.evaluate_line(y_coord)
    # print(area_map)
    # print(len([x for x in area_map.empty if x[1] == y_coord]))

    # part 2
    limit = 4000000
    # y_limit = x_limit = (0, 20)
    unknown = area_map.find_unknown(limit)
    print(unknown[0] * 4000000 + unknown[1])


if __name__ == "__main__":
    advent15()
