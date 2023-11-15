#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield tuple(line.rstrip().split(')'))

objects = { second: first for first, second in load_data('input.txt') }

def trace_root(child):
	parents = []
	while child in objects:
		child = objects[child]
		parents.append(child)
	return parents

# Part One

total = 0
for child in objects.keys():
	total += len(trace_root(child))

print(total)

# Part Two

you = set(trace_root('YOU'))
san = set(trace_root('SAN'))

print(len(you.symmetric_difference(san)))

