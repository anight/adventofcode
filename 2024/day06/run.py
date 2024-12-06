#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

import numpy as np

data = list(load_data('input.txt'))

a = np.array(data)
a = np.pad(a, 1, constant_values=('%',))

# Part One

y, x = next(iter(zip(*np.where(a == '^'))))
dx, dy = 0, -1

visited = set()

while True:
	visited |= set([(x, y)])
	fx, fy = x + dx, y + dy
	if a[fy, fx] == '%':
		break
	if a[fy, fx] == '#':
		dx, dy = -dy, dx
	else:
		x, y = fx, fy

print(len(visited))

# Part Two

def walk_is_cycled(x, y, dx, dy, trail, obstacles, try_obstacle=None):
	while True:
		if (x, y, dx, dy) in trail:
			return True
		trail |= set([(x, y, dx, dy)])
		fx, fy = x + dx, y + dy
		if a[fy, fx] == '%':
			return False
		if a[fy, fx] == '#' or (fx, fy) == try_obstacle:
			dx, dy = -dy, dx
		else:
			if try_obstacle is None and (fx, fy) not in obstacles:
				# We are about to step forward. What if there was an obstacle instead?
				obstacles[ (fx, fy) ] = walk_is_cycled(x, y, -dy, dx, trail.copy(), obstacles, try_obstacle=(fx, fy))
			x, y = fx, fy

y, x = next(iter(zip(*np.where(a == '^'))))
dx, dy = 0, -1

# The new obstruction can't be placed at the guard's starting position
obstacles = { (x, y): False }

walk_is_cycled(x, y, dx, dy, set(), obstacles)

print(sum(obstacles.values()))
