#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			match = re.match(r'^position=< ?([\d-]+), +([\d-]+)> velocity=< ?([\d-]+), +([\d-]+)>$', line)
			yield tuple(map(int, match.groups()))

import re
import numpy as np

# Part One

points = np.array(list(load_data('input.txt')), dtype=int)

prev_size = float('inf')
step = 0

while True:
	min_x, max_x = np.min(points[:,0]), np.max(points[:,0])
	size = max_x - min_x
	if size > prev_size:
		min_x, max_x = np.min(prev_points[:,0]), np.max(prev_points[:,0])
		min_y, max_y = np.min(prev_points[:,1]), np.max(prev_points[:,1])
		field = np.zeros([max_y - min_y + 1, max_x - min_x + 1], dtype=int)
		field[ (prev_points[:,1] - min_y, prev_points[:,0] - min_x) ] = 1
		break
	prev_points = points[:,:2].copy()
	prev_size = size
	points[:,:2] += points[:,2:]
	step += 1

for line in field:
	print(''.join(map(str, line)).replace('1', '#').replace('0', '.'))

# Part Two

print(step-1)
