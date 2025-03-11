#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = tuple(map(int, line.split('x')))
			yield t

# Part One

result = 0

for l, w, h in load_data('input.txt'):
	sides = l*w, l*h, w*h
	result += 2 * sum(sides) + min(sides)

print(result)

# Part Two

result = 0

for l, w, h in load_data('input.txt'):
	sides = [l, w, h]
	sides.remove(max(sides))
	result += 2 * sum(sides) + l*w*h

print(result)
