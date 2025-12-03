from math import floor


def get_fuel_for_module(mass: int) -> int:
    return floor(mass / 3) - 2


def get_fuel_for_module_and_fuel(mass: int) -> int:
    fuel = floor(mass / 3) - 2
    return fuel + get_fuel_for_module_and_fuel(fuel) if fuel > 0 else 0


def get_all_modules_fuel(list_of_mass: list[int]) -> tuple[int, int]:
    fuel: int = 0
    fuel_advanced: int = 0
    for mass in list_of_mass:
        fuel += get_fuel_for_module(mass)
        fuel_advanced += get_fuel_for_module_and_fuel(mass)
    return fuel, fuel_advanced


def calculate_fuel_requirements(input_file: str) -> tuple[int, int]:
    # Path to input file dependent on repository location
    with open(input_file, encoding="utf-8") as file:
        lines = file.readlines()

    list_of_mass: list[int] = [int(line) for line in lines]
    return get_all_modules_fuel(list_of_mass)


def advent1() -> None:
    input_file = "inputs/2019/day1.txt"
    fuel_mass, fuel_mass_including_fuel = calculate_fuel_requirements(input_file)
    print(
        f"Fuel required for all the modules: {fuel_mass}\n"
        f"Fuel required for all modules, counting in the weight "
        f"of the fuel: {fuel_mass_including_fuel}\n"
        f"We would have {(1 - fuel_mass / fuel_mass_including_fuel) * 100:.1f}% "
        f"less fuel than needed if we did not count in it's own weight!"
    )


if __name__ == "__main__":
    advent1()
