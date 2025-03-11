#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

def p(r, c):
	return ((c + r) ** 2 - c - 3 * r + 2) // 2

def code(r, c):
	n = p(r, c)
	result = 20151125
	for _ in range(n-1):
		result = (result * 252533) % 33554393
	return result

print(code(3010, 3019))

