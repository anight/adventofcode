#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield int(line)

# Part One

result = sum(load_data('input.txt'))

print(result)

# Part Two

history = set()

freq = 0

from itertools import cycle

for delta in cycle(load_data('input.txt')):
	freq += delta
	if freq in history:
		break
	history.add(freq)

print(freq)
