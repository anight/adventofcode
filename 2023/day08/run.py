#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		maps = {}
		instructions = f.readline().rstrip('\n')
		f.readline()
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' = ')
			maps[t[0]] = tuple(t[1][1:-1].split(', '))
		return instructions, maps

# Part One

instructions, maps = load_data('input.txt')

def walk(node, end):
	steps = 0
	while not end(node):
		for i in instructions:
			node = maps[node][{"L": 0, "R": 1}[i]]
			steps += 1
	return steps

print(walk('AAA', lambda node: node == 'ZZZ'))

# Part Two

cycles = []

for node in maps.keys():
	if not node.endswith('A'):
		continue
	cycles.append(walk(node, lambda node: node.endswith('Z')))

from math import lcm

print(lcm(*cycles))
