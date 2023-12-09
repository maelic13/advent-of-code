from math import lcm
from re import findall
from time import time_ns


class Node:
    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.name} = ({self.left}, {self.right})"

    def get_next(self, instruction: str) -> str:
        if instruction == "L":
            return self.left
        if instruction == "R":
            return self.right
        raise RuntimeError(f"Incorrect instruction: {instruction}")

    def is_ghost_end(self) -> bool:
        return self.name[-1] == "Z"

    def is_ghost_start(self) -> bool:
        return self.name[-1] == "A"

    def is_dead_end(self) -> bool:
        return self.name == self.left and self.name == self.right


class Network:
    def __init__(self, network: dict[str, Node] | None = None) -> None:
        self._network = network or {}

    def add_node(self, node: Node) -> None:
        self._network[node.name] = node

    def get_node(self, name: str) -> Node:
        return self._network[name]

    def follow_instructions(self, instructions: str) -> int:
        current_node = "AAA"
        instruction_position = 0
        visited_nodes: int = 0

        while current_node != "ZZZ":
            current_node = self._network[current_node].get_next(instructions[instruction_position])
            visited_nodes += 1

            instruction_position += 1
            if instruction_position >= len(instructions):
                instruction_position = 0

        return visited_nodes

    def follow_ghost_instructions(self, instructions: str) -> int:
        current_nodes = [node.name for node in self._network.values() if node.is_ghost_start()]
        distances: list[int] = []

        for node in current_nodes:
            current_node = node
            instruction_position = 0
            visited_nodes: int = 0

            while not self._network[current_node].is_ghost_end():
                current_node = (self._network[current_node]
                                .get_next(instructions[instruction_position]))
                visited_nodes += 1

                instruction_position += 1
                if instruction_position >= len(instructions):
                    instruction_position = 0

            distances.append(visited_nodes)

        return lcm(*distances)


def day8() -> None:
    with open("inputs/2023/day8.txt", "r") as file:
        lines = file.readlines()

    instructions = lines[0].strip()
    network = Network()
    for line in lines[2:]:
        network.add_node(Node(*findall("[0-9A-Z]+", line)))

    # part 1
    print(network.follow_instructions(instructions))

    # part 2
    print(network.follow_ghost_instructions(instructions))


if __name__ == "__main__":
    start = time_ns()
    day8()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
