class Move:
    def __init__(self, text_move: str) -> None:
        parameters = text_move.strip().split(" ")
        self.count = int(parameters[1])
        self.origin = int(parameters[3]) - 1
        self.target = int(parameters[5]) - 1

    def __str__(self) -> str:
        return f"move {self.count} from {self.origin} to {self.target}"


class Cargo:
    def __init__(self, stacks: list[list[str]]) -> None:
        self.stacks = stacks

    @staticmethod
    def from_text(text_cargo: list[str]) -> "Cargo":
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
        moved_boxes = self.stacks[crane_move.origin][-crane_move.count:]
        self.stacks[crane_move.origin] = self.stacks[crane_move.origin][:-crane_move.count]
        self.stacks[crane_move.target] += moved_boxes

    def get_topmost_crates(self) -> str:
        return "".join([x[-1] for x in self.stacks])


if __name__ == "__main__":
    with open("../inputs/day5.txt", "r") as file:
        lines = file.readlines()

    cargo = Cargo.from_text(lines[:lines.index("\n")])
    moves: list[Move] = [Move(x) for x in lines[lines.index("\n") + 1:]]

    # part 1
    for move in moves:
        cargo.move_crates_9000(move)
    print(cargo.get_topmost_crates())

    # part 2
    cargo = Cargo.from_text(lines[:lines.index("\n")])
    for move in moves:
        cargo.move_crates_9001(move)
    print(cargo.get_topmost_crates())
