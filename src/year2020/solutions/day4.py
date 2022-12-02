from copy import copy
import numpy as np
from typing import List

from src.infra import DataReader


def count_valid_passports(database: List, required: List, strict: bool = False) -> int:
    valid = 0
    for item in database:
        if not check_passport(item, copy(required), strict):
            valid += 1
    return valid


def check_passport(passport: List, fields: List, strict: bool) -> List:
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
        allowed = ["#", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                   "a", "b", "c", "d", "e", "f"]
        return np.all([character in allowed for character in field_value])
    if field_name == "ecl":
        return field_value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    if field_name == "pid":
        try:
            int(field_value)
            success = True
        except ValueError:
            success = False
        return len(field_value) == 9 and success
    if field_name == "cid":
        return True
    return False


if __name__ == "__main__":
    input_data = DataReader.read_txt_in_batch("day4.txt")
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    valid_passports = count_valid_passports(input_data, required_fields)
    print("Number of valid passports counting in those without cid: {}.".format(valid_passports))

    valid_strict = count_valid_passports(input_data, required_fields, strict=True)
    print("Number of strictly valid passports counting in those without cid: {}.".format(
        valid_strict))
