import string


def evaluate_prio(items: list[str]) -> int:
    score = 0
    for item in items:
        score += list(string.ascii_letters).index(item) + 1
    return score


def find_common(rucksacks: list[str]) -> str:
    for character in rucksacks[0].strip():
        if all(character in rucksack for rucksack in rucksacks[1:]):
            return character
    raise RuntimeError("No common item in rucksacks!")


def advent3() -> None:
    with open("inputs/2022/day3.txt", "r") as file:
        lines = file.readlines()

    # part 1
    errors: list[str] = []
    for line in lines:
        first_half = line.strip()[:len(line) // 2]
        second_half = line.strip()[len(line) // 2:]
        errors.append(find_common([first_half, second_half]))
    print(evaluate_prio(errors))

    # part 2
    i = 0
    errors = []
    while i < len(lines):
        errors.append(find_common(lines[i:i + 3]))
        i += 3
    print(evaluate_prio(errors))


if __name__ == "__main__":
    advent3()
