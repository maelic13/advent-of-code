from functools import cmp_to_key
import json


def compare(item1, item2) -> int:
    """
    Compare items, negative means item1 is lower, 0 equal and positive larger than item2.
    """
    if isinstance(item1, int) and isinstance(item2, int):
        return 0 if item1 == item2 else item1 - item2

    if isinstance(item1, int):
        return compare([item1], item2)
    if isinstance(item2, int):
        return compare(item1, [item2])

    for i in range(min([len(item1), len(item2)])):
        order = compare(item1[i], item2[i])
        if order == 0:
            continue
        return order
    return 0 if len(item1) == len(item2) else len(item1) - len(item2)


def advent13() -> None:
    with open("../inputs/day13.txt", "r") as file:
        lines = file.readlines()

    i = 0
    packets = []
    while i + 1 < len(lines):
        packets.append((json.loads(lines[i].strip()), json.loads(lines[i + 1].strip())))
        i += 3

    # part 1
    compare_indices: list[int] = []
    for index, packet in enumerate(packets, start=1):
        item1, item2 = packet
        if compare(item1, item2) < 0:
            compare_indices.append(index)
    print(sum(compare_indices))

    # part 2
    single_packets = [[[2]], [[6]]]
    for line in lines:
        if line == "\n":
            continue
        single_packets.append(json.loads(line.strip()))
    single_packets.sort(key=cmp_to_key(compare))
    print((single_packets.index([[2]]) + 1) * (single_packets.index([[6]]) + 1))


if __name__ == "__main__":
    advent13()
