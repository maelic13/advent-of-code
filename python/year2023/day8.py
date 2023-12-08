from time import time
from re import findall


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


class Network:
    def __init__(self, network: dict[str, Node] | None = None) -> None:
        self._network = network or {}

    def add_node(self, node: Node) -> None:
        self._network[node.name] = node

    def get_node(self, name: str) -> Node:
        return self._network[name]

    def follow_instructions(self, current_node: str, end_node: str, instructions: str) -> list[str]:
        instruction_position = 0
        visited_nodes: list[str] = []

        while current_node != end_node:
            current_node = self._network[current_node].get_next(instructions[instruction_position])
            visited_nodes.append(current_node)

            instruction_position += 1
            if instruction_position >= len(instructions):
                instruction_position = 0

        return visited_nodes


def day8() -> None:
    with open("inputs/2023/day8.txt", "r") as file:
        lines = file.readlines()

    instructions = lines[0].strip()
    network = Network()
    for line in lines[2:]:
        network.add_node(Node(*findall("[A-Z]+", line)))

    # part 1
    print(len(network.follow_instructions("AAA", "ZZZ", instructions)))


if __name__ == "__main__":
    start = time()
    day8()
    print(f"Execution time: {round((time() - start))} seconds.")
