from abc import ABCMeta, abstractmethod

from src.infra import DataReader


class PasswordValidator(metaclass=ABCMeta):
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
        return (password[par1 - 1] == symbol and password[par2 - 1] != symbol
                or password[par1 - 1] != symbol and password[par2 - 1] == symbol)


def advent2() -> None:
    data = DataReader.read_txt("day2.txt", str)
    solution = SumPasswordValidator().count_valid_passwords(data)
    print(F"Number of valid passwords method sum: {solution}")

    solution = PositionalPasswordValidator().count_valid_passwords(data)
    print(F"Number of valid passwords method position: {solution}")


if __name__ == "__main__":
    advent2()
