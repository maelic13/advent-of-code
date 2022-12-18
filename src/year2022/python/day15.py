from multiprocessing import cpu_count, Pool


import numpy as np


class Sensor:
    def __init__(self, position: tuple[int, ...], nearest_beacon: tuple[int, ...]) -> None:
        self.position = position
        self.beacon = nearest_beacon
        self.beacon_distance = self._distance(self.position, self.beacon)

    @property
    def min_x(self) -> int:
        return self.position[0] - self.beacon_distance

    @property
    def max_x(self) -> int:
        return self.position[0] + self.beacon_distance

    def guaranteed_empty(self, position: tuple[int, ...]) -> bool:
        return (position != self.beacon and position != self.position
                and self._distance(self.position, position) <= self.beacon_distance)

    def is_unknown(self, position: tuple[int, ...]) -> bool:
        return (position != self.beacon and position != self.position
                and self._distance(self.position, position) > self.beacon_distance)

    def closest_unknowns(self, limit: tuple[int, ...]) -> list[tuple[int, ...]]:
        def in_limits(coord: int) -> bool:
            return limit[0] <= coord <= limit[1]

        distance = self.beacon_distance
        unknowns: list[tuple[int, ...]] = []
        current = np.array(self.position) + np.array((distance + 1, 0))
        for step in [np.array((-1, 1)), np.array((-1, -1)), np.array((1, -1)), np.array((1, 1))]:
            for _ in range(distance + 1):
                current += step
                if in_limits(current[0]) and in_limits(current[1]):
                    unknowns.append(tuple(current))
        return unknowns

    @staticmethod
    def _distance(position1: tuple[int, ...], position2: tuple[int, ...]) -> int:
        return sum(abs(x) for x in np.array(position1) - np.array(position2))


class AreaMap:
    def __init__(self, sensors: list[Sensor]) -> None:
        self.sensors = sensors
        self.empty: set[tuple[int, ...]] = set()
        self.unknown: set[tuple[int, ...]] = set()

    def min_x(self) -> int:
        return min(x.min_x for x in self.sensors)

    def max_x(self) -> int:
        return max(x.max_x for x in self.sensors)

    @staticmethod
    def identify_empty(x_range: tuple[int, ...], y_coord: int, sensors: set[Sensor]
                       ) -> list[tuple[int, ...]]:
        empty: list[tuple[int, ...]] = []
        for x_coord in range(x_range[0], x_range[1]):
            position = (x_coord, y_coord)
            for sensor in sensors:
                if sensor.guaranteed_empty(position):
                    empty.append(position)
                    break
        return empty

    def find_empty(self, y_coord: int) -> set[tuple[int, ...]]:
        interval = (self.min_x(), self.max_x())
        line_length = abs(self.max_x() - self.min_x())
        batch_size = line_length // cpu_count()
        inputs = []
        for i in range(cpu_count()):
            inputs.append(((interval[0] + i * batch_size, interval[0] + (i + 1) * batch_size),
                           y_coord, self.sensors))
        inputs[-1] = ((inputs[-1][0][0], inputs[-1][0][1] + line_length % cpu_count()),
                      inputs[-1][1], inputs[-1][2])

        with Pool() as pool:
            results = pool.starmap(self.identify_empty, inputs)
            pool.close()
            pool.join()

        unknowns: set[tuple[int, ...]] = {x for r in results for x in r}
        return unknowns

    @staticmethod
    def identify_unknown(sensor: Sensor, sensors: set[Sensor],
                         limit: tuple[int, ...]) -> list[tuple[int, ...]]:
        to_check: list[tuple[int, ...]] = sensor.closest_unknowns(limit)
        for position in to_check:
            if all(sensor.is_unknown(position) for sensor in sensors):
                return [position]
        return []

    def find_unknown(self, limit: tuple[int, ...]) -> tuple[int, ...]:
        inputs = [(sensor, self.sensors, limit) for sensor in self.sensors]
        with Pool() as pool:
            results = pool.starmap(self.identify_unknown, inputs)
            pool.close()
            pool.join()

        unknowns: set[tuple[int, ...]] = {x for r in results for x in r}
        if not len(unknowns) == 1:
            raise RuntimeError("Unknown position could not be found.")
        return unknowns.pop()


def advent15() -> None:
    with open("../inputs/day15.txt", "r") as file:
        lines = file.readlines()

    sensors: list[Sensor] = []
    for line in lines:
        sensor_txt, beacon_txt = line.split("Sensor at x=")[1].split(": closest beacon is at x=")
        sensor_coord = sensor_txt.split(", y=")
        beacon_coord = beacon_txt.split(", y=")
        sensors.append(Sensor(position=(int(sensor_coord[0]), int(sensor_coord[1])),
                              nearest_beacon=(int(beacon_coord[0]), int(beacon_coord[1]))))
    area_map = AreaMap(sensors)

    # part 1
    y_coord = 2000000
    known_empty = area_map.find_empty(y_coord)
    print(len(known_empty))

    # part 2
    limit = (0, 4000000)
    unknown = area_map.find_unknown(limit)
    print(unknown[0] * 4000000 + unknown[1])


if __name__ == "__main__":
    advent15()
