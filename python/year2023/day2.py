from time import time_ns


class Set:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def from_string(string: str) -> "Set":
        red, green, blue = 0, 0, 0
        for cube in string.split(", "):
            num, color = cube.split(" ")
            if color == "red":
                red = int(num)
            elif color == "green":
                green = int(num)
            elif color == "blue":
                blue = int(num)
        return Set(red, green, blue)

    def power(self) -> int:
        return self.red * self.green * self.blue


class Game:
    def __init__(self, game_id: int, sets_played: list[Set]) -> None:
        self.id = game_id
        self.sets = sets_played

    @staticmethod
    def from_string(string: str) -> "Game":
        sets: list[Set] = []

        game, played_sets = string.strip().split(": ")
        game_id = int(game.split(" ")[1])

        for played_set in played_sets.split("; "):
            sets.append(Set.from_string(played_set))

        return Game(game_id, sets)

    def is_possible(self, played_set: Set) -> bool:
        for game_set in self.sets:
            if (played_set.red < game_set.red or played_set.green < game_set.green
                    or played_set.blue < game_set.blue):
                return False
        return True

    def min_necessary(self) -> Set:
        return Set(
            max(game_set.red for game_set in self.sets),
            max(game_set.green for game_set in self.sets),
            max(game_set.blue for game_set in self.sets)
        )


def day2() -> None:
    with open("inputs/2023/day2.txt", "r") as file:
        lines = file.readlines()

    task1: list[Game] = []
    task2 = 0
    for line in lines:
        game = Game.from_string(line)
        if game.is_possible(Set(12, 13, 14)):
            task1.append(game)
        task2 += game.min_necessary().power()

    # part 1
    print(sum(game.id for game in task1))
    # part 2
    print(task2)


if __name__ == "__main__":
    start = time_ns()
    day2()
    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
