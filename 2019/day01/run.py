#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield int(line)

# Part One

result = sum(map(lambda mass: mass // 3 - 2, load_data('input.txt') ))

print(result)

# Part Two

def required_fuel(mass):
	fuel = mass // 3 - 2
	if fuel <= 0:
		return 0
	return fuel + required_fuel(fuel)

result = sum(map(required_fuel, load_data('input.txt')))

print(result)

