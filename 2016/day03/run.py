#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield list(map(int, line.split()))

# Part One

def valid_triangle(a, b, c):
	return a < b + c and b < a + c and c < a + b

result = sum( valid_triangle(*sides) for sides in load_data('input.txt') )

print(result)

# Part Two

import numpy as np

data = np.array(list(load_data('input.txt')))
data = data.reshape([-1, 3, 3])
data = data.transpose([0, 2, 1])
data = data.reshape([-1, 3])

result = sum( valid_triangle(*sides) for sides in data )

print(result)
