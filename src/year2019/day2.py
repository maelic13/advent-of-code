from copy import deepcopy


class Intcode:
    def __init__(self) -> None:
        self.memory: list[int] = []
        self._backup_memory: list[int] = []
        self._instruction_length = 4
        self._iteration_limit: float = float("inf")

    def initial_state_from_file(self, path: str) -> None:
        with open(path, 'r') as file:
            lines = file.readlines()

        self.memory = [int(x) for x in lines[0].split(',')]
        self._backup_memory = deepcopy(self.memory)

    def reset(self, clear_memory: bool = True) -> None:
        if clear_memory:
            self.memory = []
        else:
            self.memory = deepcopy(self._backup_memory)
        self._instruction_length = 4
        self._iteration_limit = float("inf")

    def run(self) -> None:
        if not self.memory:
            raise RuntimeError("Internal program memory not specified.")
        iteration_counter = 0
        while iteration_counter < self._iteration_limit:
            instruction_pointer = iteration_counter * self._instruction_length
            if self.memory[instruction_pointer] == 1:
                first_number = self.memory[self.memory[instruction_pointer + 1]]
                second_number = self.memory[self.memory[instruction_pointer + 2]]
                self.memory[self.memory[instruction_pointer + 3]] = first_number + second_number
            elif self.memory[instruction_pointer] == 2:
                first_number = self.memory[self.memory[instruction_pointer + 1]]
                second_number = self.memory[self.memory[instruction_pointer + 2]]
                self.memory[self.memory[instruction_pointer + 3]] = first_number * second_number
            elif self.memory[instruction_pointer] == 99:
                break
            else:
                print("Unknown error encountered, mistake in calculation.")
                break
            iteration_counter += 1


def task1(computer: Intcode, value1: int, value2: int) -> int:
    computer.memory[1] = value1
    computer.memory[2] = value2
    computer.run()
    return computer.memory[0]


def task2(computer: Intcode) -> int:
    values_to_test = [[x, y] for x in range(0, 100) for y in range(0, 100)]
    for values in values_to_test:
        computer.reset(clear_memory=False)
        result = task1(computer, values[0], values[1])
        if result == 19690720:
            return 100 * values[0] + values[1]
    raise RuntimeError("Computation of task 2 unsuccessful.")


def advent2() -> None:
    intcode = Intcode()
    input_file = 'inputs/day2.txt'
    intcode.initial_state_from_file(input_file)

    # Tasks
    result_task1 = task1(intcode, 12, 2)
    result_task2 = task2(intcode)

    # Results
    print(f"Task 1: Original state before catching fire was: {result_task1}")
    print(f"Task 2: Computed error code is: {result_task2}")


if __name__ == "__main__":
    advent2()
