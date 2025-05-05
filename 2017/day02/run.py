#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split()))

# Part One

result = sum( max(nums) - min(nums) for nums in load_data('input.txt') )

print(result)

# Part Two

from itertools import combinations

result = 0

for nums in load_data('input.txt'):
	for a, b in combinations(nums, 2):
		if a % b == 0:
			d = a // b
			break
		if b % a == 0:
			d = b // a
			break
	result += d

print(result)
