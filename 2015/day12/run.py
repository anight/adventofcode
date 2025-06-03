#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

from json import loads

text = next(load_data('input.txt'))
j = loads(text)

def jsum(j, ignore_red=False):
	if type(j) is list:
		return sum(jsum(a, ignore_red) for a in j)
	elif type(j) is dict:
		if ignore_red and "red" in j.values():
			return 0
		return sum(jsum(a, ignore_red) for a in j.values())
	elif type(j) is int:
		return j
	return 0

print(jsum(j))

# Part Two

print(jsum(j, True))
