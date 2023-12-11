#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

from itertools import combinations

import numpy as np
a = np.array(list(load_data('input.txt')))

for x in range(a.shape[1]-1, -1, -1):
	if np.all(a[:,x] == '.'):
		a = np.hstack((a[:,:x], a[:,x:x+1], a[:,x:x+1], a[:,x+1:]))

for y in range(a.shape[0]-1, -1, -1):
	if np.all(a[y,:] == '.'):
		a = np.vstack((a[:y,:], a[y:y+1,:], a[y:y+1,:], a[y+1:,:]))

stars = list(zip(*np.where(a == '#')))

distances1 = [ abs(y0-y1) + abs(x0 - x1) for (y0, x0), (y1, x1) in combinations(stars, 2) ]

print(sum(distances1))

# Part Two

a = np.array(list(load_data('input.txt')))

stars = list(zip(*np.where(a == '#')))

distances = [ abs(y0-y1) + abs(x0-x1) for (y0, x0), (y1, x1) in combinations(stars, 2) ]

print(sum([ d + (d1 - d) * 999999 for d, d1 in zip(distances, distances1) ]))

