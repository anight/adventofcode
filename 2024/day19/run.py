#! /usr/bin/env python3

def load_data(filename):
	towels = None
	designs = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				continue
			elif towels is None:
				towels = line.split(', ')
			else:
				designs.append(line)
	return towels, designs

towels, designs = load_data('input.txt')

# Part One

from functools import cache

@cache
def is_possible(design):
	if design == '':
		return True
	for towel in towels:
		if design.startswith(towel) and is_possible(design[len(towel):]):
			return True
	return False

result = sum(map(is_possible, designs))

print(result)

# Part Two

@cache
def num_ways(design, ways=0):
	if design == '':
		return 1
	n = 0
	for towel in towels:
		if design.startswith(towel):
			ret = num_ways(design[len(towel):], ways)
			n += ret
	return ways + n

result = sum(map(num_ways, designs))

print(result)
