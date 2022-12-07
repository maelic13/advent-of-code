from typing import Optional


def are_chars_unique(characters: str) -> bool:
    return len(characters) == len(set(characters))


if __name__ == "__main__":
    with open("inputs/day6.txt", "r") as file:
        DATASTREAM = file.readline().strip()

    # part 1
    i = 0
    CHAR_NUM: Optional[int] = None
    while i + 4 < len(DATASTREAM):
        if are_chars_unique(DATASTREAM[i:i + 4]):
            CHAR_NUM = i + 4
            break
        i += 1
    print(CHAR_NUM)

    # part 2
    i = 0
    CHAR_NUM = None
    while i + 14 < len(DATASTREAM):
        if are_chars_unique(DATASTREAM[i:i + 14]):
            CHAR_NUM = i + 14
            break
        i += 1
    print(CHAR_NUM)
