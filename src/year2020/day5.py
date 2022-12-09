from typing import Any, Optional

from src.infra import DataReader


class BoardingPass:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.seat_id = row * 8 + column

    def __hash__(self) -> int:
        return hash((self.row, self.column, self.seat_id))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BoardingPass):
            return NotImplemented
        return (self.row == other.row
                and self.column == other.column
                and self.seat_id == other.seat_id)

    @classmethod
    def from_text(cls, text_boarding_pass: str) -> 'BoardingPass':
        row, column = cls._proc_pass(text_boarding_pass)
        return BoardingPass(row, column)

    @classmethod
    def _proc_pass(cls, boarding_pass: str) -> tuple[int, int]:
        row = cls._proc_str(boarding_pass[:7])
        column = cls._proc_str(boarding_pass[7:])
        return row, column

    @staticmethod
    def _proc_str(string: str) -> int:
        temp = ""
        for character in string:
            if character in ("B", "R"):
                temp += "1"
            if character in ("F", "L"):
                temp += "0"
        return int(temp, 2)


class BoardingHelper:
    def __init__(self, scanned_passes: list[BoardingPass]) -> None:
        self.boarding_passes = scanned_passes

    @staticmethod
    def from_text(text_boarding_passes: list[str]) -> "BoardingHelper":
        boarding_passes = [BoardingPass.from_text(boarding_pass)
                           for boarding_pass in text_boarding_passes]
        return BoardingHelper(boarding_passes)

    def get_highest_seat_id(self) -> int:
        return sorted(self.boarding_passes, key=lambda b_pass: b_pass.seat_id,
                      reverse=True)[0].seat_id

    def find_my_seat(self) -> Optional[int]:
        for row in range(128):
            for column in range(8):
                temp_pass = BoardingPass(row, column)
                if temp_pass not in self.boarding_passes and self._find_neighbours(temp_pass):
                    return temp_pass.seat_id
        return None

    def _find_neighbours(self, b_pass: BoardingPass) -> bool:
        needed_neighbours = 2
        for boarding_pass in self.boarding_passes:
            if boarding_pass.seat_id in (b_pass.seat_id - 1, b_pass.seat_id + 1):
                needed_neighbours -= 1
        return needed_neighbours == 0


def advent5() -> None:
    input_data = DataReader.read_txt("day5.txt", str)
    helper = BoardingHelper.from_text(input_data)

    hid = helper.get_highest_seat_id()
    print(f"Task 1: Highest seat id: {hid}")

    my_seat_id = helper.find_my_seat()
    print(f"Task 2: My seat id: {my_seat_id}")


if __name__ == "__main__":
    advent5()
