#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			tokens = line.split()
			x1, y1 = tokens[0].split(',')
			x2, y2 = tokens[2].split(',')
			yield int(x1), int(y1), int(x2), int(y2)

# Part One

import numpy as np

def coords_of_line(x1, y1, x2, y2, nodiag=False):
	if x1 != x2 and y1 != y2 and nodiag:
		return ([], [])
	def direction(c1, c2):
		if c2 > c1:
			return 1
		if c2 < c1:
			return -1
		return 0
	x, y = x1, y1
	dx, dy = direction(x1, x2), direction(y1, y2)
	ret = []
	while True:
		ret.append( (y, x) )
		if x == x2 and y == y2:
			break
		x += dx
		y += dy
	return tuple(zip(*ret))

a = np.zeros((1000, 1000), dtype=int)

for c in load_data('input.txt'):
	a[coords_of_line(*c, nodiag=True)] += 1

print(len(np.where(a > 1)[0]))

# Part Two

a = np.zeros((1000, 1000), dtype=int)

for c in load_data('input.txt'):
	a[coords_of_line(*c)] += 1

print(len(np.where(a > 1)[0]))
