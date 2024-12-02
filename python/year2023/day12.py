from copy import deepcopy
from itertools import combinations_with_replacement, permutations
from time import time


class SpringRow:
    def __init__(self, springs: list[str], backup: list[int]) -> None:
        self.backup = backup
        self.springs = springs

    def count_possible_variations(self) -> int:
        unknowns = len([spring for spring in self.springs if spring == "?"])
        valid_variations = 0

        for base_attempt in combinations_with_replacement([".", "#"], unknowns):
            for attempt in permutations(base_attempt, unknowns):
                if self._is_valid(self._get_replaced(self.springs, attempt), self.backup):
                    valid_variations += 1

        return valid_variations

    def _is_valid(self, springs: list[str], backup: list[int]) -> bool:
        current_count = 0
        count_index = 0

        for spring in [springs] + ["."]:
            if not spring == "#" and current_count > 0:
                try:
                    if not current_count == backup[count_index]:
                        return False
                except IndexError:
                    return False
                count_index += 1
                current_count = 0
            if spring == "#":
                current_count += 1

        return True

    def _get_replaced(self, springs: list[str], attempt: tuple[str]) -> list[str]:
        to_use_index = 0
        spring_variation: list[str] = []

        for spring in springs:
            if spring == "?":
                spring_variation.append(attempt[to_use_index])
                to_use_index += 1
                continue
            spring_variation.append(spring)

        return spring_variation


def day12() -> None:
    with open("inputs/2023/day12.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    # part 1
    rows: list[SpringRow] = []
    for line in lines:
        springs, backup = line.split()
        rows.append(SpringRow(list(springs), [int(x) for x in backup.split(",")]))

    print(sum(row.count_possible_variations() for row in rows))


if __name__ == "__main__":
    start = time()
    day12()
    print(f"Execution time: {round(time() - start)} seconds.")
