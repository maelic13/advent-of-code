from time import time_ns


class Report:
    def __init__(self, report: list[str]) -> None:
        self._report = report

    def sum_predicted_future_values(self) -> int:
        return sum(
            self.predict_value([int(value) for value in line.split()]) for line in self._report
        )

    def sum_predicted_past_values(self) -> int:
        return sum(
            self.predict_value([int(value) for value in line.split()][::-1])
            for line in self._report
        )

    def predict_value(self, values: list[int]) -> int:
        if all(value == 0 for value in values):
            return 0

        return values[-1] + self.predict_value([
            values[i] - values[i - 1] for i in range(1, len(values))
        ])


def day9() -> None:
    with open("inputs/2023/day9.txt", encoding="utf-8") as file:
        lines = file.readlines()
    report = Report([line.strip() for line in lines])

    # part 1
    print(report.sum_predicted_future_values())

    # part 2
    print(report.sum_predicted_past_values())


if __name__ == "__main__":
    start = time_ns()
    day9()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
