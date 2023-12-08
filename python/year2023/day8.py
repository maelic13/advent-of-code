from time import time


def day8() -> None:
    with open("inputs/2023/day8_ex.txt", "r") as file:
        lines = file.readlines()


if __name__ == "__main__":
    start = time()
    day8()
    print(f"Execution time: {round((time() - start))} seconds.")
