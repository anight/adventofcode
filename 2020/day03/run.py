#! /usr/bin/env python3

import math
import numpy as np

def load_data(filename):
	a = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			line = line.replace('#', '1').replace('.', '0')
			a.append(list(map(int, line)))
	return np.array(a, dtype=int)

def num_trees(m, dx, dy):
	y, x = 0, 0
	result = 0
	while y < m.shape[0]:
		result += m[y,x%m.shape[1]]
		x += dx
		y += dy
	return result

m = load_data('input.txt')

# Part One

print(num_trees(m, 3, 1))

# Part Two

result = 1
for dx, dy in ( (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ):
	result *= num_trees(m, dx, dy)

print(result)
