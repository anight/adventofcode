#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line.split(',')

# Part One

steps = next(load_data("input.txt"))

from collections import Counter

def distance(c):
	n = abs(c['n'] - c['s'])
	nw = abs(c['nw'] - c['se'])
	ne = abs(c['ne'] - c['sw'])
	return n+max(ne, nw)

print(distance(Counter(steps)))

# Part Two

result = 0
c = {'n': 0, 'ne': 0, 'nw': 0, 'se': 0, 'sw': 0, 's': 0}
for s in steps:
	c[s] += 1
	result = max(result, distance(c))

print(result)

