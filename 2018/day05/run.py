#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

polymer = next(load_data('input.txt'))

# Part One

def reduce(polymer):
	ret = ''
	i = 0
	while i < len(polymer)-1:
		if ord(polymer[i]) ^ ord(polymer[i+1]) == 32:
			i += 2
		else:
			ret += polymer[i]
			i += 1
	if i == len(polymer)-1:
		ret += polymer[i]
	return ret

def reduce_full(polymer):
	while True:
		new_polymer = reduce(polymer)
		if len(new_polymer) == len(polymer):
			break
		polymer = new_polymer
	return polymer

reduced = reduce_full(polymer)

print(len(reduced))

# Part Two

from string import ascii_lowercase, ascii_uppercase

best = len(polymer)

for u1, u2 in zip(ascii_lowercase, ascii_uppercase):
	new_polymer = polymer.replace(u1, '').replace(u2, '')
	reduced = reduce_full(new_polymer)
	if best > len(reduced):
		best = len(reduced)

print(best)
