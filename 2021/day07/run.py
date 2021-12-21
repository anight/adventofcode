#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().strip()
		numbers = list(map(int, line.split(',')))
		return numbers

# Part One

import numpy as np

numbers = np.array(load_data('input.txt'), dtype=int)

best_fuel = None
best_position = None

for p in range(2000):
	fuel = np.sum(np.abs(numbers - p))
	if best_fuel is None:
		best_fuel = fuel
	else:
		if best_fuel > fuel:
			best_fuel = fuel
			best_position = p

print(best_fuel)

# Part Two

best_fuel = None
best_position = None

cost = [0]
for n in range(1, 2000):
	cost.append(cost[-1] + n)
cost = np.array(cost, dtype=int)

for p in range(2000):
	fuel = np.abs(numbers - p)
	fuel = cost[fuel]
	fuel = np.sum(fuel)
	if best_fuel is None:
		best_fuel = fuel
	else:
		if best_fuel > fuel:
			best_fuel = fuel
			best_position = p

print(best_fuel)
