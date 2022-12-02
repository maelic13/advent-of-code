from abc import ABCMeta, abstractmethod
from typing import Iterable

from src.infra import DataReader


class PasswordValidator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def check_password(par1, par2, symbol, password):
        """
        Check password validity.
        """

    def count_valid_passwords(self, database: Iterable) -> int:
        valid, _ = self.validate_passwords(database)
        return len(valid)

    def validate_passwords(self, database: Iterable) -> [Iterable, Iterable]:
        valid = list()
        invalid = list()

        for item in database:
            par1, par2, symbol, password = self._parse_database_entry(item)
            if self.check_password(par1, par2, symbol, password):
                valid.append(password)
                continue
            invalid.append(password)
        return valid, invalid

    @staticmethod
    def _parse_database_entry(database_entry: str) -> [int, int, str, str]:
        temp, password = database_entry.split(": ")
        temp, symbol = temp.split(" ")
        par1, par2 = temp.split("-")
        return int(par1), int(par2), symbol, password


class SumPasswordValidator(PasswordValidator):
    @staticmethod
    def check_password(minimum, maximum, symbol, password):
        return minimum <= password.count(symbol) <= maximum


class PositionalPasswordValidator(PasswordValidator):
    @staticmethod
    def check_password(index1, index2, symbol, password):
        return (password[index1 - 1] == symbol and password[index2 - 1] != symbol
                or password[index1 - 1] != symbol and password[index2 - 1] == symbol)


if __name__ == "__main__":
    data = DataReader.read_txt("day2.txt", str)
    solution = SumPasswordValidator().count_valid_passwords(data)
    print("Number of valid passwords method sum: {}".format(solution))

    solution = PositionalPasswordValidator().count_valid_passwords(data)
    print("Number of valid passwords method position: {}".format(solution))
