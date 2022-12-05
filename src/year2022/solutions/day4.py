def convert(sectors: str) -> list[int]:
    min_value, max_value = sectors.split("-")
    return list(range(int(min_value), int(max_value) + 1))


def find_overlap(sectors: list[list[int]]):
    elements = set()
    for sector in sectors:
        for element in sector:
            elements.add(element)

    overlap_elements = list()
    for element in elements:
        if all([element in sector for sector in sectors]):
            overlap_elements.append(element)
    return sorted(overlap_elements)


if __name__ == "__main__":
    with open("../inputs/day4.txt", "r") as file:
        lines = file.readlines()

    # part1
    complete_overlap_counter = 0
    for line in lines:
        first_sectors, second_sectors = line.strip().split(",")
        first_sectors = convert(first_sectors)
        second_sectors = convert(second_sectors)
        overlap = find_overlap([first_sectors, second_sectors])
        if overlap == first_sectors or overlap == second_sectors:
            complete_overlap_counter += 1
    print(complete_overlap_counter)

    # part2
    counter = 0
    for line in lines:
        first_sectors, second_sectors = line.strip().split(",")
        first_sectors = convert(first_sectors)
        second_sectors = convert(second_sectors)
        if find_overlap([first_sectors, second_sectors]):
            counter += 1
    print(counter)
