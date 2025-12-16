from functools import reduce
from itertools import combinations
from operator import xor
from time import time_ns
from typing import TYPE_CHECKING

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from advent_of_code.infra import read_input, report_times

if TYPE_CHECKING:
    from collections.abc import Iterable


class Machine:
    def __init__(
        self,
        result_lights: int,
        buttons_array: np.ndarray,
        joltages: np.ndarray,
    ) -> None:
        self._buttons_array = buttons_array
        self._joltages = joltages
        self._result_lights = result_lights

    def __str__(self) -> str:
        formatted_result = self._to_binary_string(self._result_lights, len(self._joltages))
        return (
            f"Machine:\n"
            f"\tResult lights: {formatted_result}\n"
            f"\tButtons arrays: {self._buttons_array}\n"
            f"\tJoltages: {self._joltages}\n"
        )

    @staticmethod
    def _to_binary(binary_iterable: Iterable[int]) -> int:
        return sum(val << i for i, val in enumerate(binary_iterable))

    @staticmethod
    def _to_binary_string(mask: int, length: int) -> str:
        return f"{mask:b}".zfill(length)

    @classmethod
    def from_string(cls, machine: str) -> Machine:
        parts = machine.split(" ")

        result_lights = cls._to_binary([1 if char == "#" else 0 for char in parts[0][1:-1]])
        joltages = np.array([int(char) for char in parts[-1][1:-1].split(",")], dtype=int)

        buttons_array = []
        for button_string in parts[1:-1]:
            indices = [int(char) for char in button_string[1:-1].split(",")]
            array = np.zeros(len(joltages), dtype=int)
            array[indices] = 1
            buttons_array.append(array)

        return cls(result_lights, np.array(buttons_array), joltages)

    def fewest_presses_to_result(self) -> int:
        buttons_binary = [self._to_binary(button) for button in self._buttons_array]

        for num_presses in range(1, len(self._buttons_array) + 1):
            for combination in combinations(buttons_binary, num_presses):
                if reduce(xor, combination) == self._result_lights:
                    return num_presses

        msg = "No combination of buttons leads to solution."
        raise RuntimeError(msg)

    def fewest_presses_to_joltage(self) -> int:
        n_buttons = len(self._buttons_array)

        bounds = Bounds(lb=0, ub=np.inf)
        constraints = LinearConstraint(self._buttons_array.T, self._joltages, self._joltages)
        integrality = np.ones(n_buttons, dtype=int)
        objective_coefficients = np.ones(n_buttons, dtype=int)

        result = milp(
            c=objective_coefficients,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality,
        )

        if result.success:
            return int(result.fun)

        msg = "No combination of buttons leads to solution."
        raise RuntimeError(msg)


def day10() -> None:
    start = time_ns()

    # read and parse file
    inputs = read_input(2025, 10, example=False).splitlines()
    machines = [Machine.from_string(machine) for machine in inputs]
    file_read_time = time_ns() - start

    # part 1
    print(sum(machine.fewest_presses_to_result() for machine in machines))
    part1_time = time_ns() - start

    # part 2
    print(sum(machine.fewest_presses_to_joltage() for machine in machines))
    part2_time = time_ns() - start

    # Report times
    report_times(file_read_time, part1_time, part2_time)


if __name__ == "__main__":
    day10()
