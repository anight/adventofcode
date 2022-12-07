#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.strip()
			a.append(list(map(int, line)))
		return np.array(a, dtype=int)

# Part One

import numpy as np

field = load_data('input.txt')

field_padded = np.pad(field, 1, 'constant', constant_values=9)

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

kernel = np.zeros([3, 3], dtype=int)

rolled = rolling_window(field_padded, kernel)

c, up, down, left, right = rolled[...,1,1], rolled[...,0,1], rolled[...,2,1], rolled[...,1,0], rolled[...,1,2]

low_points = np.logical_and(np.logical_and(c < up, c < down), np.logical_and(c < left, c < right))

risk_levels = field[np.where(low_points)] + 1

print(np.sum(risk_levels))

# Part Two

basins_locations = {}
basins = []

for y, x in zip(*np.where(low_points)):
	if (y, x) in basins_locations:
		continue
	basin = {}
	to_check = [(y, x)]
	basins.append(basin)
	while len(to_check) > 0:
		ly, lx = to_check.pop()
		assert (ly, lx) not in basins_locations
		basin[(ly, lx)] = None
		basins_locations[(ly, lx)] = None
		for dy, dx in ( (-1, 0), (1, 0), (0, -1), (0, 1) ):
			if (ly+dy, lx+dx) not in basin and (ly+dy, lx+dx) not in to_check and field_padded[1+ly+dy,1+lx+dx] < 9:
				to_check.append( (ly+dy, lx+dx) )

sorted_basins = sorted([len(b) for b in basins], reverse=True)[:3]

print(sorted_basins[0] * sorted_basins[1] * sorted_basins[2])

