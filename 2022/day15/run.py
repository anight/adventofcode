#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line[len('Sensor at x='):].split(': closest beacon is at x=')
			sensor = tuple(map(int, t[0].split(', y=')))
			beacon = tuple(map(int, t[1].split(', y=')))
			yield sensor, beacon

# Part One

from itertools import pairwise, product

the_row = 2_000_000
beacons_in_the_row = set()
all_intervals = []
for (sx, sy), (bx, by) in load_data('input.txt'):
	if by == the_row:
		beacons_in_the_row |= set([bx])
	distance = abs(sx - bx) + abs(sy - by)
	interval = (sx - distance + abs(sy - the_row), sx + distance - abs(sy - the_row))
	if interval[0] <= interval[1]:
		all_intervals.append(interval)

all_intervals = sorted(all_intervals)

while True:
	for i1, i2 in pairwise(all_intervals):
		if i2[0] > i1[1]:
			continue
		new = (min(i1[0], i2[0]), max(i1[1], i2[1]))
		all_intervals.remove(i1)
		all_intervals.remove(i2)
		all_intervals.append(new)
		break
	else:
		break
	all_intervals = sorted(all_intervals)

total = 0
for f, t in all_intervals:
	r = t - f + 1
	for bx in beacons_in_the_row:
		if f <= bx <= t:
			r -= 1
	total += r

print(total)

# Part Two

lines_p = []
lines_n = []
for (sx, sy), (bx, by) in load_data('input.txt'):
	distance = abs(sx - bx) + abs(sy - by)
	t = sx, sy-distance
	b = sx, sy+distance
	def line_p(p):
		x, y = p
		return 1, y - x
	def line_n(p):
		x, y = p
		return -1, y + x
	lines_p.extend([ line_p(t), line_p(b) ])
	lines_n.extend([ line_n(t), line_n(b) ])

for lp, ln in product(lines_p, lines_n):
	k1, b1 = lp
	k2, b2 = ln
	x = (b2 - b1) / (k1 - k2)
	y = k1 * x + b1
	if x < 0 or x > 4_000_000 or y < 0 or y > 4_000_000:
		continue
	def find_invisible_cell(x, y):
		for dx, dy in product(range(-2, 3), repeat=2):
			candidate = (x + dx, y + dy)
			def visible(p):
				x, y = p
				for (sx, sy), (bx, by) in load_data('input.txt'):
					distance = abs(sx - bx) + abs(sy - by)
					distance_p = abs(sx - x) + abs(sy - y)
					if distance_p <= distance:
						return True
				return False
			if not visible(candidate):
				return candidate
		return None
	result = find_invisible_cell(int(x), int(y))
	if result is not None:
		break
else:
	raise Exception("not found")

print(result[0] * 4_000_000 + result[1])
