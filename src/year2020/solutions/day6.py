import numpy as np
from typing import List

from src.infra import DataReader


class QuestionnaireHelper:
    def __init__(self, answers: List[List[str]]) -> None:
        self.answers = answers

    def count_group_answers(self, ans_type: str) -> int:
        count = 0
        for group_answers in self.answers:
            count += len(self._get_answers(group_answers, ans_type))
        return count

    @staticmethod
    def _get_answers(group_answers: List[str], ans_type: str) -> set:
        result = set()
        for answer in group_answers:
            for character in answer:
                if ans_type == "unique":
                    result.add(character)
                elif ans_type == "common":
                    result.add(character) if np.all(
                        [character in group for group in group_answers]) else None
        return result


if __name__ == "__main__":
    input_data = DataReader.read_txt_in_batch("day6.txt")
    qh = QuestionnaireHelper(input_data)

    unique_sum = qh.count_group_answers("unique")
    print("Task 1: Sum of unique group answers: {}".format(unique_sum))

    common_sum = qh.count_group_answers("common")
    print("Task 2: Sum of common group answers: {}".format(common_sum))
