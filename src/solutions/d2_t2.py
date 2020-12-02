from src.infra.api import DataReader

from src.solutions.d2_t1 import PasswordValidator


class PositionalPasswordValidator(PasswordValidator):
    @staticmethod
    def check_password(index1, index2, symbol, password):
        return (password[index1 - 1] == symbol and password[index2 - 1] != symbol
                or password[index1 - 1] != symbol and password[index2 - 1] == symbol)


if __name__ == "__main__":
    data = DataReader.read_txt("d2_t1.txt", str)
    solution = PositionalPasswordValidator().count_valid_passwords(data)
    print("Number of valid passwords: {}".format(solution))
