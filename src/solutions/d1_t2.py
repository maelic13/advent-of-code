from src.infra.api import DataReader

from src.solutions.d1_t1 import expense_record


if __name__ == "__main__":
    data = DataReader.read_txt("d1_t1.txt", int)
    solution = expense_record(data, 3)
    print("Solution is: {}".format(solution))
