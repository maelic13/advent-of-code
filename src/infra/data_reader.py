from typing import Any, Callable


class DataReader:
    @staticmethod
    def read_txt(file_name: str, output_format_function: Callable[[str], Any]) -> list[Any]:
        with open("inputs/" + file_name, "r") as file:
            return [output_format_function(item) for item in file.readlines()]

    @staticmethod
    def read_txt_in_batch(file_name: str, batch_limiter: str = "\n", sample_limiter: str = " "
                          ) -> list[Any]:
        with open("inputs/" + file_name, "r") as file:
            lines = file.readlines()

        full_data: list[list[str]] = []
        batch: list[str] = []
        for line in lines:
            if line == batch_limiter:
                full_data.append(batch)
                batch = []
                continue
            batch += line.rstrip().split(sample_limiter)
            if lines[-1] == line:
                full_data.append(batch)
                batch = []
        return full_data
