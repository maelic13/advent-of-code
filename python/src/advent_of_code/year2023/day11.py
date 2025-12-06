from itertools import combinations
from time import time


class GalaxyImage:
    def __init__(self, galaxy_image: list[list[str]]) -> None:
        self._galaxy_image = galaxy_image
        self._galaxies: list[tuple[int, int]] = self._find_galaxies(galaxy_image)

    @classmethod
    def from_measurement(cls, measurement: list[str]) -> GalaxyImage:
        galaxy_image: list[list[str]] = [list(line) for line in measurement]
        galaxy_image = [list(i) for i in zip(*galaxy_image, strict=False)]
        galaxy_image = cls._expand_galaxy_image_rows(galaxy_image)
        galaxy_image = [list(i) for i in zip(*galaxy_image, strict=False)]
        galaxy_image = cls._expand_galaxy_image_rows(galaxy_image)

        return GalaxyImage(galaxy_image)

    def sum_shortest_distances_between_galaxies(self) -> int:
        distances = 0

        for g1, g2 in combinations(self._galaxies, 2):
            distances += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

        return distances

    @staticmethod
    def _find_galaxies(galaxy_image: list[list[str]]) -> list[tuple[int, int]]:
        galaxies: list[tuple[int, int]] = []

        for i, line in enumerate(galaxy_image):
            for j, char in enumerate(line):
                if char == "#":
                    galaxies.append((i, j))

        return galaxies

    @staticmethod
    def _expand_galaxy_image_rows(galaxy_image: list[list[str]]) -> list[list[str]]:
        new_image: list[list[str]] = []

        for row in galaxy_image:
            new_image.append(row)
            if any(char != "." for char in row):
                continue
            new_image.append(row)

        return new_image


def day11() -> None:
    with open("inputs/2023/day11.txt", encoding="utf-8") as file:
        lines = [line.strip() for line in file]
    image = GalaxyImage.from_measurement(lines)

    # part 1
    print(image.sum_shortest_distances_between_galaxies())


if __name__ == "__main__":
    start = time()
    day11()
    print(f"Execution time: {round(time() - start)} seconds.")
