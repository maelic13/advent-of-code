from copy import deepcopy


class Intcode:
    def __init__(self):
        self._memory = None
        self._backup_memory = None
        self._instruction_length = 4
        self._iteration_limit = None

    def initial_state_from_file(self, path):
        with open(path, 'r') as file:
            self._memory = file.readlines()
            self._memory = self._memory[0].split(',')
            self._memory = [int(x) for x in self._memory]
            self._backup_memory = deepcopy(self._memory)

    def initial_state(self, data):
        self._memory = data

    def reset(self, clear_memory=True):
        if clear_memory:
            self._memory = None
        else:
            self._memory = deepcopy(self._backup_memory)
        self._instruction_length = 4
        self._iteration_limit = None

    def run(self):
        if not self._memory:
            raise RuntimeError("Internal program memory not specified.")
        iteration_counter = 0
        while self._iteration_limit is None or iteration_counter < self._iteration_limit:
            instruction_pointer = iteration_counter * self._instruction_length
            if self._memory[instruction_pointer] == 1:
                first_number = self._memory[self._memory[instruction_pointer + 1]]
                second_number = self._memory[self._memory[instruction_pointer + 2]]
                self._memory[self._memory[instruction_pointer + 3]] = first_number + second_number
            elif self._memory[instruction_pointer] == 2:
                first_number = self._memory[self._memory[instruction_pointer + 1]]
                second_number = self._memory[self._memory[instruction_pointer + 2]]
                self._memory[self._memory[instruction_pointer + 3]] = first_number * second_number
            elif self._memory[instruction_pointer] == 99:
                break
            else:
                print("Unknown error encountered, mistake in calculation.")
                break
            iteration_counter += 1

    def get_specific_data(self, address):
        return self._memory[address]

    def get_all_data(self):
        return self._memory

    def replace_in_memory(self, address, value):
        self._memory[address] = value


def task1(computer, value1, value2):
    computer.replace_in_memory(1, value1)
    computer.replace_in_memory(2, value2)
    computer.run()
    return computer.get_specific_data(0)


def task2(computer):
    values_to_test = [[x, y] for x in range(0, 100) for y in range(0, 100)]
    for values in values_to_test:
        computer.reset(clear_memory=False)
        result = task1(computer, values[0], values[1])
        if result == 19690720:
            return 100 * values[0] + values[1]
    raise RuntimeError("Computation of task 2 unsuccessful.")


if __name__ == "__main__":
    computer = Intcode()
    input_file = 'input.txt'
    computer.initial_state_from_file(input_file)

    # Tasks
    result_task1 = task1(computer, 12, 2)
    result_task2 = task2(computer)

    # Results
    print("Task 1: Original state before catching fire was: {}".format(result_task1))
    print("Task 2: Computed error code is: {}".format(result_task2))
