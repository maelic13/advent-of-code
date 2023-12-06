from time import time_ns


class Diagnostic:
    def __init__(self, log: list[str]) -> None:
        self._epsilon: str = ""
        self._gamma: str = ""
        self._log = log

    def gamma(self) -> str:
        if not self._gamma:
            self._gamma = self._calculate_gamma(self._log)
        return self._gamma

    def epsilon(self) -> str:
        if not self._epsilon:
            self._epsilon = self._calculate_epsilon(self.gamma())
        return self._epsilon

    def oxygen_rating(self) -> int:
        sub_log = self._log
        position = 0

        while len(sub_log) > 1:
            gamma = self._calculate_gamma(sub_log)
            buff: list[str] = []
            for number in sub_log:
                if number[position] == gamma[position]:
                    buff.append(number)
            sub_log = buff
            position += 1
        return int(sub_log[0], base=2)

    def co2_rating(self) -> int:
        sub_log = self._log
        position = 0

        while len(sub_log) > 1:
            epsilon = self._calculate_epsilon(self._calculate_gamma(sub_log))
            buff: list[str] = []
            for number in sub_log:
                if number[position] == epsilon[position]:
                    buff.append(number)
            sub_log = buff
            position += 1
        return int(sub_log[0], base=2)

    @staticmethod
    def _calculate_gamma(log: list[str]) -> str:
        gamma = ""
        log = list(map(list, zip(*log)))

        for line in log:
            if sum(int(bit) for bit in line) >= len(log[0]) / 2:
                gamma += "1"
            else:
                gamma += "0"

        return gamma

    @staticmethod
    def _calculate_epsilon(gamma: str) -> str:
        epsilon = ""
        for bit in gamma:
            if bit == "1":
                epsilon += "0"
            else:
                epsilon += "1"
        return epsilon


def advent3() -> None:
    with open("inputs/2021/day3.txt", "r") as file:
        diagnostic = Diagnostic([line.strip() for line in file.readlines()])

    # part 1
    print(int(diagnostic.gamma(), base=2) * int(diagnostic.epsilon(), base=2))
    # part 2
    print(diagnostic.oxygen_rating() * diagnostic.co2_rating())


if __name__ == "__main__":
    start = time_ns()
    advent3()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
