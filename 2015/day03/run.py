#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

line = next(load_data('input.txt'))

# Part One

pos = 0
houses = set([pos])

for ch in line:
	pos += 1 * 1j ** ">v<^".index(ch)
	houses.add(pos)

print(len(houses))

# Part Two

pos = [0, 0]
houses = set([pos[0]])

for i, ch in enumerate(line):
	pos[i%2] += 1 * 1j ** ">v<^".index(ch)
	houses.add(pos[i%2])

print(len(houses))
