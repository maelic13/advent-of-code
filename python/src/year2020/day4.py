from copy import copy
from time import time_ns


def count_valid_passports(
    database: list[list[str]], required: list[str], strict: bool = False
) -> int:
    valid = 0
    for item in database:
        if not check_passport(item, copy(required), strict):
            valid += 1
    return valid


def check_passport(passport: list[str], fields: list[str], strict: bool) -> list:
    for item in passport:
        for field in fields:
            if strict and not validate_field(item):
                continue
            if field in item:
                fields.remove(field)
    return fields


def validate_field(field: str) -> bool:
    field_name, field_value = field.split(":")
    if field_name == "byr":
        return 1920 <= int(field_value) <= 2002
    if field_name == "iyr":
        return 2010 <= int(field_value) <= 2020
    if field_name == "eyr":
        return 2020 <= int(field_value) <= 2030
    if field_name == "hgt":
        if "cm" in field_value:
            return 150 <= int(field_value.replace("cm", "")) <= 193
        if "in" in field_value:
            return 59 <= int(field_value.replace("in", "")) <= 76
        return False
    if field_name == "hcl":
        if "#" not in field_value:
            return False
        allowed = [
            "#",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]
        return all(character in allowed for character in field_value)
    if field_name == "ecl":
        return field_value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    if field_name == "pid":
        try:
            int(field_value)
            success = True
        except ValueError:
            success = False
        return len(field_value) == 9 and success
    return field_name == "cid"


def advent4() -> None:
    with open("inputs/2020/day4.txt", encoding="utf-8") as file:
        data = file.readlines()

    input_data: list[list[str]] = []
    batch: list[str] = []
    for line in data:
        if not line.strip():
            input_data.append(batch)
            batch = []
            continue
        batch += line.strip().split()
        if data[-1] == line:
            input_data.append(batch)

    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    valid_passports = count_valid_passports(input_data, required_fields)
    print(f"Number of valid passports counting in those without cid: {valid_passports}.")

    valid_strict = count_valid_passports(input_data, required_fields, strict=True)
    print(f"Number of strictly valid passports counting in those without cid: {valid_strict}.")


if __name__ == "__main__":
    start = time_ns()
    advent4()
    print(f"Execution time: {round((time_ns() - start) // 1000000)} milliseconds.")
