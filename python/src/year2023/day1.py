from time import time_ns

from regex import findall

word_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def word2int(word: str) -> int:
    """
    Convert word to integer.
    :param word: word to convert
    :return: integer
    """
    for num_word, num in word_num.items():
        word = word.replace(num_word, num)
    return int(word)


def day1() -> None:
    with open("inputs/2023/day1.txt", encoding="utf-8") as file:
        lines = file.readlines()

    task1: list[int] = []
    task2: list[int] = []
    word_pattern = "|".join(word_num.keys())
    for line in lines:
        found_digits = findall(r"[1-9]", line.strip())
        found_words = findall(word_pattern, line.strip(), overlapped=True)

        first = min(found_digits + found_words, key=line.index)
        last = max(found_digits + found_words, key=line.rfind)

        task1.append(int(found_digits[0] + found_digits[-1]))
        task2.append(word2int(first + last))

    # part 1
    print(sum(task1))
    # part 2
    print(sum(task2))


if __name__ == "__main__":
    start = time_ns()
    day1()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
