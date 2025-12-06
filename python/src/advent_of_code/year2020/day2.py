from abc import ABC, abstractmethod
from time import time_ns


class PasswordValidator(ABC):
    @staticmethod
    @abstractmethod
    def check_password(par1: int, par2: int, symbol: str, password: str) -> bool:
        """
        Check password validity.
        """

    def count_valid_passwords(self, database: list[str]) -> int:
        valid, _ = self.validate_passwords(database)
        return len(valid)

    def validate_passwords(self, database: list[str]) -> tuple[list[str], list[str]]:
        valid: list[str] = []
        invalid: list[str] = []

        for item in database:
            par1, par2, symbol, password = self._parse_database_entry(item)
            if self.check_password(par1, par2, symbol, password):
                valid.append(password)
                continue
            invalid.append(password)
        return valid, invalid

    @staticmethod
    def _parse_database_entry(database_entry: str) -> tuple[int, int, str, str]:
        temp, password = database_entry.split(": ")
        temp, symbol = temp.split(" ")
        par1, par2 = temp.split("-")
        return int(par1), int(par2), symbol, password


class SumPasswordValidator(PasswordValidator):
    @staticmethod
    def check_password(par1: int, par2: int, symbol: str, password: str) -> bool:
        return par1 <= password.count(symbol) <= par2


class PositionalPasswordValidator(PasswordValidator):
    @staticmethod
    def check_password(par1: int, par2: int, symbol: str, password: str) -> bool:
        return (password[par1 - 1] == symbol and password[par2 - 1] != symbol) or (
            password[par1 - 1] != symbol and password[par2 - 1] == symbol
        )


def advent2() -> None:
    with open("inputs/2020/day2.txt", encoding="utf-8") as file:
        data = file.readlines()

    solution = SumPasswordValidator().count_valid_passwords(data)
    print(f"Number of valid passwords method sum: {solution}")

    solution = PositionalPasswordValidator().count_valid_passwords(data)
    print(f"Number of valid passwords method position: {solution}")


if __name__ == "__main__":
    start = time_ns()
    advent2()
    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
