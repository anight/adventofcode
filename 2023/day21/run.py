#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

import numpy as np
a = np.array(list(load_data('input.txt')))

def neighbours(x, y):
	yield x+1, y
	yield x-1, y
	yield x, y+1
	yield x, y-1

y, x = next(zip(*np.where(a == 'S')))

def plots(x, y, steps):
	visited = [ set(), { (x, y) } ]

	for _ in range(steps):
		ring = { (x, y) for vx, vy in visited[-1] for x, y in neighbours(vx, vy) if a[y % a.shape[0], x % a.shape[1]] != '#' }
		visited.append( ring - visited[-2] )

	result = set()
	for i in range(len(visited)-1, -1, -2):
		result |= visited[i]

	return result

print(len(plots(x, y, 64)))

# Part Two

steps = 26501365

size = a.shape[0]

# A lot of assumptions to make things work

assert a.shape[0] == a.shape[1]

assert size % 2 == 1
assert x == size // 2 and y == size // 2

assert set(a[0,:]) == set('.')
assert set(a[y,:]) == set('.S')
assert set(a[size-1,:]) == set('.')

assert set(a[:,0]) == set('.')
assert set(a[:,x]) == set('.S')
assert set(a[:,size-1]) == set('.')

# steps = first + big_steps * period + last

first = size
period = size * 2
big_steps = (steps - first) // period
last = steps - first - big_steps * period

xc = x + 10 * size
yc = y + 10 * size

visited = plots(xc, yc, first + last)

def n_cells(nx, ny):
	global xc, yc, size
	ix, iy = xc // size + nx, yc // size + ny
	return len({ (px, py) for px, py in visited if px // size == ix and py // size == iy })

total = n_cells(-2, 0) + n_cells(2, 0) + n_cells(0, -2) + n_cells(0, 2) + \
	(n_cells(-2, -1) + n_cells(1, -2) + n_cells(2, 1) + n_cells(-1, 2)) * (2 + 2 * big_steps) + \
	(n_cells(-1, -1) + n_cells(1, -1) + n_cells(1, 1) + n_cells(-1, 1)) * (1 + 2 * big_steps) + \
	n_cells(0, 0) * (2 * big_steps + 1) ** 2 + n_cells(1, 0) * (2 * big_steps + 2) ** 2

print(total)

