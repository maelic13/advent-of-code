from time import time_ns


def is_report_safe(rep: list[int], dampened: bool = True) -> bool:
    if len(rep) < 2:
        return True

    if rep[1] < rep[0]:
        rep = list(reversed(rep))

    for i in range(len(rep) - 1):
        if rep[i] > rep[i + 1] or not 1 <= (rep[i + 1] - rep[i]) <= 3:
            if dampened:
                return False
            dampened = True

    return True


def day2() -> None:
    with open("inputs/2024/day2.txt", "r") as file:
        lines = file.readlines()

    reports: list[list[int]] = []
    for report in lines:
        reports.append([int(x) for x in report.strip().split(" ")])

    # part 1
    print(sum(is_report_safe(report) for report in reports))

    # part 2
    print(sum(is_report_safe(report, dampened=False) for report in reports))

if __name__ == "__main__":
    start = time_ns()
    day2()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
