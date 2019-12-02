
with open("input.txt", "r") as input_file:
    masses = [int(mass) for mass in input_file.readlines() if mass]

def calc_fuel(mass):

    fuel = mass // 3 - 2
    if fuel <= 0:
        yield 0

    while fuel > 0:

        yield fuel
        fuel = fuel // 3 - 2

# part 1
simple_fuel = sum(next(calc_fuel(mass)) for mass in masses)
print(f"part 1: {simple_fuel}")

# part 2
compound_fuel = sum(([sum(calc_fuel(mass)) for mass in masses]))
print(f"part 2: {compound_fuel}")
