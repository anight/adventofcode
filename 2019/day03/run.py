#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield [ (t[0], int(t[1:])) for t in line.rstrip().split(',') ]

def render(w):
	ret = {}
	x, y, steps = 0, 0, 0
	for d, n in w:
		dx, dy = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}[d]
		for _ in range(n):
			ret[(x, y)] = steps
			x += dx
			y += dy
			steps += 1
	return ret

w1, w2 = load_data('input.txt')

w1r = render(w1)
w2r = render(w2)

def find_min_value(f):
	result = 1e10
	for x, y in set(w1r.keys()).intersection(set(w2r.keys())):
		if x == 0 and y == 0:
			continue
		value = f(x, y)
		result = min(value, result)
	return result

# Part One

result = find_min_value(lambda x, y: abs(x) + abs(y))

print(result)

# Part Two

result = find_min_value(lambda x, y: w1r[(x, y)] + w2r[(x, y)])

print(result)
