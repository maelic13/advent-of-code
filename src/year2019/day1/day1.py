import math


def get_fuel_for_module(mass):
    return math.floor(mass / 3) - 2


def get_fuel_for_module_and_fuel(mass):
    fuel = math.floor(mass / 3) - 2
    return fuel + get_fuel_for_module_and_fuel(fuel) if fuel > 0 else 0


def get_all_modules_fuel(list_od_mass):
    fuel = 0
    fuel_advanced = 0
    for mass in list_od_mass:
        fuel += get_fuel_for_module(mass)
        fuel_advanced += get_fuel_for_module_and_fuel(mass)
    return fuel, fuel_advanced


def calculate_fuel_requirements(input_file):
    # Path to input file dependent on repository location
    with open(input_file, 'r') as file:
        input = file.readlines()
        list_of_mass = []
        for str in input:
            list_of_mass.append(int(str))
        return get_all_modules_fuel(list_of_mass)


if __name__ == "__main__":
    input_file = 'input.txt'
    fuel, fuel_including_fuel = calculate_fuel_requirements(input_file)
    print("Fuel required for all the modules: {}\n"
          "Fuel required for all modules, counting in the weight of the fuel: {}\n"
          "We would have {:.1f}% less fuel than needed if we did not count in it's own weight!"
          .format(fuel, fuel_including_fuel, (1 - fuel/fuel_including_fuel)*100))
