#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

import numpy as np
field = np.array(list(load_data('input.txt')))
field = np.pad(field, 1, 'constant', constant_values='.')

# Part One

y, x = list(zip(*np.where(field == 'S')))[0]

def pipe_direction(x, y, dx, dy):
	ret = []
	if field[y,x] in '-LFS' and field[y,x+1] in '-J7' and (dx, dy) != (-1, 0):
		ret.append((1, 0))
	if field[y,x] in '|7FS' and field[y+1,x] in '|JL' and (dx, dy) != (0, -1):
		ret.append((0, 1))
	if field[y,x] in '-J7S' and field[y,x-1] in '-LF' and (dx, dy) != (1, 0):
		ret.append((-1, 0))
	if field[y,x] in '|JLS' and field[y-1,x] in '|7F' and (dx, dy) != (0, 1):
		ret.append((0, -1))
	return ret

def path(x, y, dx, dy):
	while True:
		yield x, y
		new_dx, new_dy = pipe_direction(x, y, dx, dy)[0]
		x, y, dx, dy = x+new_dx, y+new_dy, new_dx, new_dy

pd0, pd1 = pipe_direction(x, y, 0, 0)

path0 = iter(path(x+pd0[0], y+pd0[1], *pd0))
path1 = iter(path(x+pd1[0], y+pd1[1], *pd1))

steps = 1

while next(path0) != next(path1):
	steps += 1

print(steps)

# Part Two

def path(x, y, dx, dy):
	while True:
		yield x, y, dx, dy
		pd = pipe_direction(x, y, dx, dy)
		if len(pd) == 0:
			break
		new_dx, new_dy = pd[0]
		x, y, dx, dy = x+new_dx, y+new_dy, new_dx, new_dy

def trace(x, y, pd, color_left, color_right):
	dx, dy = pd
	for x, y, dx, dy in path(x+dx, y+dy, dx, dy):
		paintboard[y, x] = '@'
		def paint(color, x, y):
			if paintboard[y,x] == ' ':
				paintboard[y,x] = '#*'[color]
		paint(color_left, x-dy, y+dx)
		paint(color_right, x+dy, y-dx)

paintboard = np.full_like(field, ' ')

pd0, pd1 = pipe_direction(x, y, 0, 0)

trace(x, y, pd0, 1, 0)
trace(x, y, pd1, 0, 1)

while True:
	painted = 0
	for y, x in zip(*np.where(paintboard[1:-1,1:-1] == ' ')):
		x += 1
		y += 1
		if paintboard[y,x-1] == '#' or paintboard[y-1,x] == '#' or paintboard[y,x+1] == '#' or paintboard[y+1,x] == '#':
			paintboard[y,x] = '#'
			painted += 1
		elif paintboard[y,x-1] == '*' or paintboard[y-1,x] == '*' or paintboard[y,x+1] == '*' or paintboard[y+1,x] == '*':
			paintboard[y,x] = '*'
			painted += 1
	if painted == 0:
		break

inside_color = {'#': '*', '*': '#'}[paintboard[1,1]]

print(len(np.where(paintboard == inside_color)[0]))
