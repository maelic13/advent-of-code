def convert(sectors: str) -> list[int]:
    min_value, max_value = sectors.split("-")
    return list(range(int(min_value), int(max_value) + 1))


def find_overlap(sectors: list[list[int]]):
    elements: set[int] = set()
    for sector in sectors:
        for element in sector:
            elements.add(element)

    overlap_elements: list[int] = []
    for element in elements:
        if all(element in sector for sector in sectors):
            overlap_elements.append(element)
    return sorted(overlap_elements)


def advent4() -> None:
    with open("../inputs/day4.txt", "r") as file:
        lines = file.readlines()

    # part 1
    complete_overlap_counter: int = 0
    for line in lines:
        first, second = line.strip().split(",")
        first_sectors = convert(first)
        second_sectors = convert(second)
        overlap = find_overlap([first_sectors, second_sectors])
        if overlap in (first_sectors, second_sectors):
            complete_overlap_counter += 1
    print(complete_overlap_counter)

    # part 2
    counter = 0
    for line in lines:
        first, second = line.strip().split(",")
        first_sectors = convert(first)
        second_sectors = convert(second)
        if find_overlap([first_sectors, second_sectors]):
            counter += 1
    print(counter)


if __name__ == "__main__":
    advent4()
