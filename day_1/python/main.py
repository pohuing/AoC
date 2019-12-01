from math import floor


def calculate_fuel_fuel(weight, lookup_table = {8:0, 7:0, 6:0, 5:0, 4:0, 3:0, 2:0, 1:0, 0:0}):
    if weight in lookup_table:
        return lookup_table[weight]
    else:
        direct_requirement = floor(weight / 3) - 2
        lookup_table[weight] = calculate_fuel_fuel(direct_requirement) + direct_requirement
        return lookup_table[weight]


if __name__ == "__main__":
    total_fuel = 0
    with open("./day_1/input.txt", "r") as f:
        for line in f:
            total_fuel += calculate_fuel_fuel(int(line))
            
    print(total_fuel)