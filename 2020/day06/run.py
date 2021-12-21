#! /usr/bin/env python3

import operator

def load_data(filename, op):
	with open(filename, 'r') as f:
		group = None
		for line in f:
			line = line.strip()
			if line == '':
				yield group
				group = None
				continue
			if group is None:
				group = set(line)
			else:
				group = op(group, set(line))
		if len(group) > 0:
			yield group

# Part One

result = 0
for group in load_data('input.txt', operator.__ior__):
	result += len(group)

print(result)

# Part Two

result = 0
for group in load_data('input.txt', operator.__iand__):
	result += len(group)

print(result)
