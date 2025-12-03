class Move:
    def __init__(self, count: int, origin: int, target: int) -> None:
        self.count = count
        self.origin = origin
        self.target = target

    @staticmethod
    def from_text(text_move: str) -> Move:
        parameters = text_move.strip().split(" ")
        count = int(parameters[1])
        origin = int(parameters[3]) - 1
        target = int(parameters[5]) - 1
        return Move(count, origin, target)


class Cargo:
    def __init__(self, stacks: list[list[str]]) -> None:
        self.stacks = stacks

    @staticmethod
    def from_text(text_cargo: list[str]) -> Cargo:
        text_cargo.reverse()
        stacks: list[list[str]] = [[] for _ in range(len(text_cargo[0]) // 4)]
        for line in text_cargo[1:]:
            i = 1
            while i < len(line):
                if line[i] == " ":
                    i += 4
                    continue
                stacks[i // 4].append(line[i])
                i += 4
        return Cargo(stacks)

    def move_crates_9000(self, crane_move: Move) -> None:
        for _ in range(crane_move.count):
            crate = self.stacks[crane_move.origin].pop()
            self.stacks[crane_move.target].append(crate)

    def move_crates_9001(self, crane_move: Move) -> None:
        moved_boxes = self.stacks[crane_move.origin][-crane_move.count :]
        self.stacks[crane_move.origin] = self.stacks[crane_move.origin][: -crane_move.count]
        self.stacks[crane_move.target] += moved_boxes

    def get_topmost_crates(self) -> str:
        return "".join([x[-1] for x in self.stacks])


def advent5() -> None:
    with open("inputs/2022/day5.txt", encoding="utf-8") as file:
        lines = file.readlines()

    cargo = Cargo.from_text(lines[: lines.index("\n")])
    moves: list[Move] = [Move.from_text(x) for x in lines[lines.index("\n") + 1 :]]

    # part 1
    for move in moves:
        cargo.move_crates_9000(move)
    print(cargo.get_topmost_crates())

    # part 2
    cargo = Cargo.from_text(lines[: lines.index("\n")])
    for move in moves:
        cargo.move_crates_9001(move)
    print(cargo.get_topmost_crates())


if __name__ == "__main__":
    advent5()
