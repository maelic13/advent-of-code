from typing import Optional


def are_chars_unique(characters: str) -> bool:
    return len(characters) == len(set(characters))


def advent6() -> None:
    with open("../inputs/day6.txt", "r") as file:
        datastream = file.readline().strip()

    # part 1
    i = 0
    char_num: Optional[int] = None
    while i + 4 < len(datastream):
        if are_chars_unique(datastream[i:i + 4]):
            char_num = i + 4
            break
        i += 1
    print(char_num)

    # part 2
    i = 0
    char_num = None
    while i + 14 < len(datastream):
        if are_chars_unique(datastream[i:i + 14]):
            char_num = i + 14
            break
        i += 1
    print(char_num)


if __name__ == "__main__":
    advent6()
