from copy import deepcopy
from math import prod
from typing import Callable


class Monkey:
    def __init__(self, items: list[int], operation: tuple[str, ...], test: tuple[int, int, int],
                 relief: Callable[[int], int] = lambda x: x // 3) -> None:
        self.item_divider = test[0]
        self.monkey_targets = [test[1], test[2]]
        self.inspected_items = 0
        self.items = items
        self.operation = self.parse_operation(*operation)
        self.relief = relief
        self.test = self.parse_test(*test)

    def __repr__(self) -> str:
        return f"Monkey({self.items})"

    def turn(self) -> list[tuple[int, int]]:
        """
        :return: new item value and index of monkey to receive the item
        """
        thrown_items: list[tuple[int, int]] = []
        for item in self.items:
            self.inspected_items += 1
            new_item = self.relief(self.operation(item))
            thrown_items.append((new_item, self.test(new_item)))
        self.items = []
        return thrown_items

    def catch_item(self, item: int) -> None:
        self.items.append(item)

    @staticmethod
    def parse_operation(item1: str, operator: str, item2: str) -> Callable[[int], int]:
        """
        This solution expects only multiplication and addition in operation since level
        of worry should increase.
        """
        if item1 == "old" and item2 == "old":
            if operator == "*":
                return lambda x: x * x
            return lambda x: x + x
        if operator == "*":
            return lambda x: x * int(item2)
        return lambda x: x + int(item2)

    @staticmethod
    def parse_test(divider: int, true_result: int, false_result: int) -> Callable[[int], int]:
        return lambda x: true_result if x % divider == 0 else false_result


def make_smaller(item: int, dividers: list[int]) -> int:
    needed_dividers = [x for x in dividers if item % x == 0]
    return prod(needed_dividers)


def go_rounds(orig_monkeys: list[Monkey], rounds: int) -> list[Monkey]:
    monkeys = deepcopy(orig_monkeys)
    for _ in range(rounds):
        for monkey in monkeys:
            for item, monkey_index in monkey.turn():
                monkeys[monkey_index].catch_item(item)
    return monkeys


def advent11() -> None:
    with open("../inputs/day11.txt", "r") as file:
        lines = file.readlines()

    i = 0
    monkeys: list[Monkey] = []
    while i + 6 <= len(lines):
        monkey_info = [info.strip() for info in lines[i:i + 6]]

        items = [int(item) for item in monkey_info[1].split("Starting items: ")[1].split(",")]
        operation = tuple(item for item in monkey_info[2].split("Operation: new = ")[1].split())
        test = (int(monkey_info[3].split()[-1]), int(monkey_info[4].split()[-1]),
                int(monkey_info[5].split()[-1]))
        monkeys.append(Monkey(items, operation, test))

        i += 7

    # part 1
    inspected = sorted([x.inspected_items for x in go_rounds(monkeys, rounds=20)], reverse=True)
    print(inspected[0] * inspected[1])

    # part 2
    mod = prod([x.item_divider for x in monkeys])
    for monkey in monkeys:
        monkey.relief = lambda x: x % mod

    inspected = sorted([x.inspected_items for x in go_rounds(monkeys, rounds=10000)], reverse=True)
    print(inspected[0] * inspected[1])


if __name__ == "__main__":
    advent11()
