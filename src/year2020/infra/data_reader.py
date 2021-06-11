class DataReader:
    @staticmethod
    def read_txt(file_name, output_format_function):
        file = open("../inputs/" + file_name)
        return [output_format_function(item) for item in file.read().splitlines()]

    @staticmethod
    def read_txt_in_batch(file_name, batch_limiter="\n", sample_limiter=" "):
        file = open("../inputs/" + file_name)
        lines = file.readlines()

        full_data = list()
        batch = list()
        for line in lines:
            if line == batch_limiter:
                full_data.append(batch)
                batch = list()
                continue
            batch += line.rstrip().split(sample_limiter)
            if lines[-1] == line:
                full_data.append(batch)
                batch = list()
        return full_data
