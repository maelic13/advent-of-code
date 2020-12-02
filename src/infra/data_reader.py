class DataReader:
    @staticmethod
    def read_txt(file_name, output_format_function):
        file = open("../inputs/" + file_name)
        return [output_format_function(item) for item in file.read().splitlines()]
