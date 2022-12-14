#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			items = line.split(' -> ')
			yield [ tuple(map(int, t.split(','))) for t in items ]

# Part One

def gen_cave(load_data):
	cave = {}
	maxy = 0
	for coords in load_data:
		cx, cy = coords[0]
		cave[(cx, cy)] = 1
		for (x, y) in coords[1:]:
			def direction(n, old_n):
				if n > old_n:
					return 1
				elif n < old_n:
					return -1
				return 0
			dx = direction(x, cx)
			dy = direction(y, cy)
			while True:
				cx += dx
				cy += dy
				if maxy < cy:
					maxy = cy
				cave[(cx, cy)] = 1
				if (cx, cy) == (x, y):
					break
	return cave, maxy

def sand_step(x, y):
	if (x, y+1) not in cave:
		return (x, y+1)
	if (x-1, y+1) not in cave:
		return (x-1, y+1)
	if (x+1, y+1) not in cave:
		return (x+1, y+1)
	return (x, y)

cave, maxy = gen_cave(load_data('input.txt'))

total = 0
while True:
	sand = (500, 0)
	while True:
		next_sand = sand_step(*sand)
		if next_sand == sand:
			break
		sand = next_sand
		if sand[1] > maxy:
			break
	if sand[1] > maxy:
		break
	cave[sand] = 2
	total += 1

print(total)

# Part Two

cave, maxy = gen_cave(load_data('input.txt'))

total = 0
while True:
	sand = (500, 0)
	while True:
		next_sand = sand_step(*sand)
		if next_sand == sand:
			break
		sand = next_sand
		if sand[1] == maxy+1:
			break
	cave[sand] = 2
	total += 1
	if sand == (500, 0):
		break

print(total)
