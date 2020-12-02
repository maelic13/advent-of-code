from src.infra.api import DataReader

data = DataReader.read_txt("d1_t1.txt", int)
while data:
    number = data.pop()
    if 2020 - number in data:
        print("Result is: {}".format((2020 - number) * number))
        break
