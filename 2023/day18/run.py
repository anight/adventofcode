#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split()
			yield t[0], int(t[1]), int(t[2][2:-2], 16), int(t[2][-2])

# Part One

f = {}
colored = {}
x, y = 0, 0

minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')

for c, n, _, _ in load_data('input.txt'):
	dx, dy = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}[c]
	for step in range(n):
		cell = (x, y)
		colored[ (x+dy, y-dx) ] = 1
		colored[ (x-dy, y+dx) ] = 2
		f[cell] = '#'
		minx = min(minx, x)
		miny = min(miny, y)
		maxx = max(maxx, x)
		maxy = max(maxy, y)
		x += dx
		y += dy
		colored[ (x+dy, y-dx) ] = 1
		colored[ (x-dy, y+dx) ] = 2

for x in range(minx-1, maxx+1):
	outside_color = colored.get( (x, miny-1), None)
	if outside_color is not None:
		break
else:
	raise Exception("oops")

inside_color = 3 - outside_color

def neighbours(x, y):
	dx, dy = 1, 0
	for _ in range(4):
		yield x + dx, y + dy
		dx, dy = -dy, dx

to_paint = { cell for cell, v in colored.items() if v == inside_color and f.get(cell, None) is None }

while len(to_paint) > 0:
	cell = next(iter(to_paint))
	f[cell] = '#'
	to_paint -= set([cell])
	for n_cell in neighbours(*cell):
		if f.get(n_cell, None) is None:
			to_paint |= set([n_cell])

print(len(f))

# Part Two

figure = []
x, y = 0, 0
length = 0

for _, _, meters, direction in load_data('input.txt'):
	dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
	x += meters * dx
	y += meters * dy
	figure.append( (x, y) )
	length += meters

def area(coords):
	a = 0
	n = len(coords)
	for i in range(n):
		j = (i + 1) % n
		a += coords[i][0] * coords[j][1]
		a -= coords[j][0] * coords[i][1]
	return abs(a) // 2

print(area(figure) + length // 2 + 1)
