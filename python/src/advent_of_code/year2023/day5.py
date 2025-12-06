from functools import partial
from multiprocessing import Pool
from time import time


class Map:
    def __init__(self, name: str) -> None:
        self.name = name
        self.rules: list[tuple[range, range]] = []

    @property
    def source(self) -> str:
        return self.name.split("-to-")[0]

    @property
    def destination(self) -> str:
        return self.name.split("-to-")[1]

    def add_rule(self, rule: str) -> None:
        destination, source, size = rule.split(" ")
        self.rules.append((
            range(int(source), int(source) + int(size)),
            range(int(destination), int(destination) + int(size)),
        ))

    def get_destination(self, source: int) -> int:
        for rule in self.rules:
            if source in rule[0]:
                return rule[1].start + source - rule[0].start
        return source


def seed_to_location(maps: list[Map], seed: int) -> int:
    current_value = seed
    for sd_map in maps:
        current_value = sd_map.get_destination(current_value)
    return current_value


def day5() -> None:
    with open("inputs/2023/day5.txt", encoding="utf-8") as file:
        lines = file.readlines()

    seeds = [int(seed) for seed in lines[0].strip().split(": ")[1].split()]

    maps: dict[str, Map] = {}
    current_name = ""
    for line in lines[2:]:
        if "map" in line:
            current_name = line.strip().split()[0]
            maps[current_name] = Map(current_name)
            continue

        if not line.strip():
            continue

        maps[current_name].add_rule(line.strip())

    # part 1
    with Pool() as pool:
        locations = pool.map(partial(seed_to_location, list(maps.values())), seeds)
        pool.close()
        pool.join()
    print(min(locations))

    # part 2
    range_seeds: list[int] = []
    for i in range(0, len(seeds), 2):
        range_seeds += list(range(seeds[i], seeds[i] + seeds[i + 1]))

    with Pool() as pool:
        locations = pool.map(partial(seed_to_location, list(maps.values())), range_seeds)
        pool.close()
        pool.join()
    print(min(locations))


if __name__ == "__main__":
    start = time()
    day5()
    print(f"Execution time: {round(time() - start)} seconds.")
