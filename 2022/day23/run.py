#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

# Part One

elves = {}
for y, line in enumerate(load_data('input.txt')):
	for x, ch in enumerate(line):
		if ch == '#':
			elves[(x, y)] = None

def next_state(i, elves):
	def planned(x, y, i):
		lookup = (
			(x-1, y-1, x, y-1, x+1, y-1), # N
			(x-1, y+1, x, y+1, x+1, y+1), # S
			(x-1, y-1, x-1, y, x-1, y+1), # W
			(x+1, y-1, x+1, y, x+1, y+1), # E
		)
		result = []
		for j in range(4):
			nx1, ny1, nx2, ny2, nx3, ny3 = lookup[(i + j) % 4]
			if (nx1, ny1) not in elves and (nx2, ny2) not in elves and (nx3, ny3) not in elves:
				result.append( (nx2, ny2) )
		if len(result) == 0 or len(result) == 4:
			return None
		return result[0]

	intentions = {}
	for x, y in elves.keys():
		p = planned(x, y, i)
		if p is not None:
			elves[(x, y)] = p
			intentions[p] = intentions.get(p, 0) + 1

	new_elves = {}
	minx, maxx = float('inf'), -float('inf')
	miny, maxy = float('inf'), -float('inf')
	for (x, y), v in elves.items():
		if v is not None:
			nx, ny = v
			if intentions[(nx, ny)] == 1:
				x, y = nx, ny
		new_elves[(x, y)] = None
		if minx > x:
			minx = x
		if maxx < x:
			maxx = x
		if miny > y:
			miny = y
		if maxy < y:
			maxy = y

	return new_elves, (maxx - minx + 1), (maxy - miny + 1)

for i in range(10):
	elves, w, h = next_state(i, elves)

print(w * h - len(elves))

# Part Two

i += 1

while True:
	new_elves, _, _ = next_state(i, elves)
	i += 1
	if new_elves == elves:
		break
	elves = new_elves

print(i)
