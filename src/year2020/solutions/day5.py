from typing import List, Optional, Tuple

from src.year2020.infra.api import DataReader


class BoardingPass:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.id = row * 8 + column

    def __hash__(self):
        return hash((self.row, self.column, self.id))

    def __eq__(self, other):
        if not isinstance(other, BoardingPass):
            return NotImplemented
        return self.row == other.row and self.column == other.column and self.id == other.id

    @classmethod
    def init_from_string(cls, bpass: str) -> 'BoardingPass':
        row, column = cls._proc_pass(bpass)
        return BoardingPass(row, column)

    @classmethod
    def _proc_pass(cls, bpass: str) -> Tuple[int, int]:
        row = cls._proc_str(bpass[:7])
        column = cls._proc_str(bpass[7:])
        return row, column

    @staticmethod
    def _proc_str(string: str) -> int:
        temp = ""
        for character in string:
            if character == "B" or character == "R":
                temp += "1"
            if character == "F" or character == "L":
                temp += "0"
        return int(temp, 2)


class BoardingHelper:
    def __init__(self, scanned_passes: List) -> None:
        self.boarding_passes = [BoardingPass.init_from_string(bpass) for bpass in scanned_passes]

    def get_highest_seat_id(self) -> int:
        return sorted(self.boarding_passes, key=lambda b_pass: b_pass.id, reverse=True)[0].id

    def find_my_seat(self) -> Optional[int]:
        for row in range(128):
            for column in range(8):
                temp_pass = BoardingPass(row, column)
                if temp_pass not in self.boarding_passes and self._find_neighbours(temp_pass):
                    return temp_pass.id
        return None

    def _find_neighbours(self, b_pass: BoardingPass) -> bool:
        needed_neighbours = 2
        for boarding_pass in self.boarding_passes:
            if boarding_pass.id == b_pass.id - 1 or boarding_pass.id == b_pass.id + 1:
                needed_neighbours -= 1
        return needed_neighbours == 0


if __name__ == "__main__":
    input_data = DataReader.read_txt("day5.txt", str)
    b_helper = BoardingHelper(input_data)

    hid = b_helper.get_highest_seat_id()
    print("Task 1: Highest seat id: {}".format(hid))

    my_seat_id = b_helper.find_my_seat()
    print("Task 2: My seat id: {}".format(my_seat_id))
