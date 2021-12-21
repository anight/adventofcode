#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		foldings = None
		dots = []
		for line in f:
			line = line.strip()
			if line == '':
				foldings = []
				continue
			if foldings is None:
				x, y = line.split(',')
				dots.append( (int(x), int(y)) )
			else:
				t = line.split()
				d = t[2].split('=')
				foldings.append( (d[0], int(d[1])) )
		return np.array(dots, dtype=int), foldings

# Part One

import numpy as np

dots, foldings = load_data('input.txt')

a = np.zeros([2000, 2000], dtype=int)

a[dots[:,1], dots[:,0]] = 1

def fold(a, axis, coord):
	if axis == 'x':
		return a[:,:coord] + np.flip(a[:,coord+1:2*coord+1], axis=1)
	else:
		return a[:coord,:] + np.flip(a[coord+1:2*coord+1,:], axis=0)

for axis, coord in foldings[:1]:
	a = fold(a, axis, coord)

print(len(np.where(a != 0)[0]))

# Part Two

for axis, coord in foldings[1:]:
	a = fold(a, axis, coord)

for y in range(a.shape[0]):
	for x in range(a.shape[1]):
		if a[y,x] != 0:
			print('#', end='')
		else:
			print(' ', end='')
	print()
