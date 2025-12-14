import operator
from itertools import combinations
from math import prod
from time import time_ns

import numpy as np

from advent_of_code.infra import read_input, report_times

type Point3D = tuple[int, int, int]


class JunctionBoxClustering:
    def __init__(self, datapoints: list[Point3D]) -> None:
        self._datapoints = datapoints
        self._distances: list[tuple[Point3D, Point3D, float]] | None = None

    @staticmethod
    def _euclidean_distance(d1: Point3D, d2: Point3D) -> float:
        return np.sqrt((d1[0] - d2[0]) ** 2 + (d1[1] - d2[1]) ** 2 + (d1[2] - d2[2]) ** 2)

    def _calculate_distances(
        self,
    ) -> list[tuple[Point3D, Point3D, float]]:
        if self._distances is None:
            distances: list[tuple[Point3D, Point3D, float]] = []
            for i, j in combinations(range(len(self._datapoints)), 2):
                distances.append((
                    self._datapoints[i],
                    self._datapoints[j],
                    self._euclidean_distance(self._datapoints[i], self._datapoints[j]),
                ))
            self._distances = sorted(distances, key=operator.itemgetter(2))
        return self._distances

    @staticmethod
    def _process_connection(
        d1: Point3D,
        d2: Point3D,
        clusters: list[set[Point3D]],
    ) -> None:
        cluster1 = None
        cluster2 = None

        for cluster in clusters:
            if d1 in cluster:
                cluster1 = cluster
            if d2 in cluster:
                cluster2 = cluster

        if cluster1 is not None and cluster1 is cluster2:
            return

        if cluster1 is not None and cluster2 is not None:
            cluster1.update(cluster2)
            clusters.remove(cluster2)
            return

        if cluster1 is not None:
            cluster1.add(d2)
        elif cluster2 is not None:
            cluster2.add(d1)
        else:
            clusters.append({d1, d2})

    def get_clusters(self, steps: int) -> list[set[Point3D]]:
        clusters: list[set[Point3D]] = []
        distances = self._calculate_distances()

        for i in range(steps):
            d1, d2, _ = distances[i]
            self._process_connection(d1, d2, clusters)

        return clusters

    def get_last_connecting_boxes(self) -> tuple[Point3D, Point3D]:
        clusters: list[set[Point3D]] = []
        distances = self._calculate_distances()

        for i in range(len(distances)):
            d1, d2, _ = distances[i]
            self._process_connection(d1, d2, clusters)

            if len(clusters) == 1 and len(clusters[0]) == len(self._datapoints):
                return d1, d2

        msg = "Junction boxes could not be connected to single cluster."
        raise RuntimeError(msg)


def day8() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 8, example=False).splitlines()
    datapoints: list[Point3D] = []
    for line in inputs:
        x, y, z = line.split(",")
        datapoints.append((int(x), int(y), int(z)))
    file_read_time = time_ns() - start

    clustering = JunctionBoxClustering(datapoints)

    # part 1
    clusters = clustering.get_clusters(steps=1000)
    cluster_lengths = sorted([len(c) for c in clusters], reverse=True)
    print(prod(cluster_lengths[:3]))
    part1_time = time_ns() - start

    # part 2
    b1, b2 = clustering.get_last_connecting_boxes()
    print(b1[0] * b2[0])
    part2_time = time_ns() - start

    # Report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day8()
