from time import time_ns


class QuestionnaireHelper:
    def __init__(self, answers: list[list[str]]) -> None:
        self.answers = answers

    def count_group_answers(self, ans_type: str) -> int:
        count = 0
        for group_answers in self.answers:
            count += len(self._get_answers(group_answers, ans_type))
        return count

    @staticmethod
    def _get_answers(group_answers: list[str], ans_type: str) -> set[str]:
        result = set()
        for answer in group_answers:
            for character in answer:
                if (ans_type == "unique" or ans_type == "common"
                        and all(character in group for group in group_answers)):
                    result.add(character)
        return result


def advent6() -> None:
    with open("inputs/2020/day6.txt", "r") as file:
        lines = file.readlines()

    data: list[list[str]] = []
    batch: list[str] = []
    for line in lines:
        if not line.strip():
            data.append(batch)
            batch = []
            continue
        batch += line.strip().split()
        if lines[-1] == line:
            data.append(batch)
    helper = QuestionnaireHelper(data)

    unique_sum = helper.count_group_answers("unique")
    print(f"Task 1: Sum of unique group answers: {unique_sum}")

    common_sum = helper.count_group_answers("common")
    print(f"Task 2: Sum of common group answers: {common_sum}")


if __name__ == "__main__":
    start = time_ns()
    advent6()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
