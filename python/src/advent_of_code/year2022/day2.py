from itertools import product
from time import time_ns


class RPSPlayer:
    win_score = 6
    draw_score = 3
    lose_score = 0

    rock_score = 1
    paper_score = 2
    scissors_score = 3

    rock = ["A", "X"]
    paper = ["B", "Y"]
    scissors = ["C", "Z"]

    wins = (
        list(product(rock, scissors)) + list(product(paper, rock)) + list(product(scissors, paper))
    )
    draws = (
        list(product(rock, rock)) + list(product(paper, paper)) + list(product(scissors, scissors))
    )
    losses = (
        list(product(scissors, rock)) + list(product(rock, paper)) + list(product(paper, scissors))
    )

    @classmethod
    def evaluate(cls, move: str, opponent_move: str) -> int:
        score = cls.get_move_score(move)
        if (move, opponent_move) in cls.wins:
            score += cls.win_score
        elif (move, opponent_move) in cls.draws:
            score += cls.draw_score
        else:
            score += cls.lose_score
        return score

    @classmethod
    def get_move_score(cls, move: str) -> int:
        if move in cls.rock:
            return cls.rock_score
        if move in cls.paper:
            return cls.paper_score
        return cls.scissors_score

    @classmethod
    def evaluate_with_result(cls, opponent_move: str, result: str) -> int:
        if result == "X":
            move = next(x[0] for x in cls.losses if opponent_move == x[1])
        elif result == "Y":
            move = next(x[0] for x in cls.draws if opponent_move == x[1])
        else:
            move = next(x[0] for x in cls.wins if opponent_move == x[1])

        return cls.evaluate(move, opponent_move)


def advent2() -> None:
    start = time_ns()

    with open("inputs/2022/day2.txt", encoding="utf-8") as file:
        lines = file.readlines()

    data: list[list[str]] = [line.rstrip().split(" ") for line in lines]
    file_read_time = round((time_ns() - start) // 1000)

    # part 1
    total_score = 0
    for opponent_choice, choice in data:
        total_score += RPSPlayer.evaluate(choice, opponent_choice)
    part1_time = round((time_ns() - start) // 1000) - file_read_time
    print(total_score)

    # part 2
    total_score = 0
    for opponent_choice, game_result in data:
        total_score += RPSPlayer.evaluate_with_result(opponent_choice, game_result)
    part2_time = round((time_ns() - start) // 1000) - part1_time - file_read_time
    print(total_score)

    print()
    print(f"Total time: {file_read_time + part1_time + part2_time} microseconds.")
    print(f"File read time: {file_read_time} microseconds.")
    print(f"Execution time: {part1_time + part2_time} microseconds.")
    print()
    print(f"Part 1 execution time: {part1_time} microseconds.")
    print(f"Part 2 execution time: {part2_time} microseconds.")


if __name__ == "__main__":
    advent2()
