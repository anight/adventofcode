#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line.split(' ')
			yield t[0], int(t[1])

# Part One

from math import copysign

def one_step(hx, hy, tx, ty):
	if abs(hx-tx) == 2 or abs(hy-ty) == 2:
		tx += int(copysign(hx != tx, hx-tx))
		ty += int(copysign(hy != ty, hy-ty))
	return tx, ty

hx, hy = 0, 0
tx, ty = 0, 0
seen = {}
for direction, cnt in load_data('input.txt'):
	dx, dy = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}[direction]
	for _ in range(cnt):
		hx += dx
		hy += dy
		tx, ty = one_step(hx, hy, tx, ty)
		seen[(tx, ty)] = None

print(len(seen))

# Part Two

rope = [ [0, 0] for _ in range(10) ]
seen = {}
for direction, cnt in load_data('input.txt'):
	dx, dy = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}[direction]
	for _ in range(cnt):
		rope[0][0] += dx
		rope[0][1] += dy
		for i in range(len(rope)-1):
			rope[i+1][0], rope[i+1][1] = one_step(rope[i][0], rope[i][1], rope[i+1][0], rope[i+1][1])
		seen[(rope[9][0], rope[9][1])] = None

print(len(seen))
