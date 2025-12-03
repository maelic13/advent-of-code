from collections import deque


class CPU:
    def __init__(self, initial_value) -> None:
        self.command_queue: deque[str] = deque()
        self.current_command: tuple[str, int] = ("noop", 0)
        self.register = initial_value
        self.registry_history: list[int] = [initial_value]

    def add_command(self, command: str) -> None:
        self.command_queue.append(command)

    def execute(self) -> None:
        while self.command_queue or self.current_command:
            self.current_command = (self.current_command[0], self.current_command[1] + 1)
            if self.current_command[1] >= self._command_duration(self.current_command[0]):
                self._finish_command(self.current_command[0])
                try:
                    self.current_command = self.command_queue.popleft(), 0
                except IndexError:
                    return
            self.registry_history.append(self.register)

    @staticmethod
    def _command_duration(command: str) -> int:
        if command == "noop":
            return 1
        if "addx" in command:
            return 2
        msg = "Unknown command."
        raise RuntimeError(msg)

    def _finish_command(self, command: str) -> None:
        if command == "noop":
            return

        _, value = command.split()
        self.register += int(value)


def advent10() -> None:
    with open("inputs/2022/day10.txt", encoding="utf-8") as file:
        commands = file.readlines()

    # part 1
    cpu = CPU(initial_value=1)
    for command in commands:
        cpu.add_command(command.strip())
    cpu.execute()
    print(sum(cpu.registry_history[x] * x for x in [20, 60, 100, 140, 180, 220]))

    # part 2
    crt: list[list[str]] = [[] for _ in range(6)]
    for tick, position in enumerate(cpu.registry_history[1:]):
        char = "."
        if tick % 40 in {position - 1, position, position + 1}:
            char = "#"
        crt[tick // 40].append(char)

    for pixel_row in crt:
        print("".join(pixel for pixel in pixel_row))


if __name__ == "__main__":
    advent10()
