from src.infra import DataReader


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
    input_data = DataReader.read_txt_in_batch("day6.txt")
    helper = QuestionnaireHelper(input_data)

    unique_sum = helper.count_group_answers("unique")
    print(f"Task 1: Sum of unique group answers: {unique_sum}")

    common_sum = helper.count_group_answers("common")
    print(f"Task 2: Sum of common group answers: {common_sum}")


if __name__ == "__main__":
    advent6()
