#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

from math import gcd, atan2

asteroids = {}
for y, line in enumerate(load_data('input.txt')):
	for x, ch in enumerate(line):
		if ch == '#':
			asteroids[(x, y)] = 0

# Part One

best = (0, (-1, -1))
for bx, by in asteroids.keys():
	total = 0
	for x, y in asteroids.keys():
		if (bx, by) == (x, y):
			continue
		g = gcd(bx-x, by-y)
		dx, dy = (x-bx) // g, (y-by) // g
		for i in range(1, g):
			if (bx + i * dx, by + i * dy) in asteroids:
				break
		else:
			total += 1
	best = max(best, (total, (bx, by)))

print(best[0])

# Part Two

bx, by = best[1]
by_angle = {}
for x, y in asteroids.keys():
	if (bx, by) == (x, y):
		continue
	key = atan2(x-bx, y-by)
	g = gcd(bx-x, by-y)
	if key not in by_angle:
		by_angle[key] = {g: (x, y)}
	else:
		by_angle[key][g] = (x, y)

vaporized = 0
while vaporized < 200:
	for angle in sorted(by_angle.keys(), reverse=True):
		d = by_angle[angle]
		if len(d) == 0:
			continue
		closest = sorted(d.keys())[0]
		vaporized += 1
		x, y = d[closest]
		if vaporized == 200:
			break
		del d[closest]

print(100 * x + y)
