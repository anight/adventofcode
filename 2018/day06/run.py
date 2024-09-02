#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(', ')
			yield int(t[0]), int(t[1])

import numpy as np

coords = np.array(list(load_data('input.txt')))

# Part One

def distances(coords, pad):
	coords = np.transpose(coords)[:, :, np.newaxis, np.newaxis]
	min_x, max_x = np.min(coords[0]) - pad, np.max(coords[0]) + pad
	min_y, max_y = np.min(coords[1]) - pad, np.max(coords[1]) + pad
	grid = np.mgrid[min_y:max_y+1, min_x:max_x+1][:, np.newaxis, :, :]
	return np.abs(grid[0] - coords[1]) + np.abs(grid[1] - coords[0])

def area(coords, pad):
	d = distances(coords, pad)
	mask = d == np.min(d, axis=0)
	mask[:, *np.where(np.sum(mask, axis=0) > 1)] = False
	return np.sum(mask, axis=(1, 2))

a1 = area(coords, 0)
a2 = area(coords, 1)

a1[np.where(a1 != a2)] = 0
print(np.max(a1))

# Part Two

def area2(coords, pad):
	d = distances(coords, pad)
	s = np.sum(d, axis=0)
	return np.sum(s < 10000)

print(area2(coords, 0))
