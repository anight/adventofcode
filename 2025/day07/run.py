#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

data = load_data('input.txt')
start_line = next(data)
beams = set([start_line.index('S')])

total = 0

for line in data:
	splitters = set([ i for i, c in enumerate(line) if c == '^'])
	for i in splitters:
		if i in beams:
			total += 1
			beams |= {i-1, i+1}
			beams -= {i}

print(total)

# Part Two

from collections import defaultdict

data = load_data('input.txt')
start_line = next(data)
beams = defaultdict(int)
beams[start_line.index('S')] = 1

for line in data:
	splitters = set([ i for i, c in enumerate(line) if c == '^'])
	for i in splitters:
		beams[i-1] += beams[i]
		beams[i+1] += beams[i]
		beams[i] = 0

print(sum(beams.values()))
