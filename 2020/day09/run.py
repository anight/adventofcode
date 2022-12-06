#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield int(line)

# Part One

from itertools import combinations

nums = list(load_data('input.txt'))

for i in range(25, len(nums)):
	n = nums[i]
	if all(n != a + b for a, b in combinations(nums[i-25:i], 2)):
		break

print(n)

# Part Two

from_i, to_i = 0, 2

while True:
	s = sum(nums[from_i:to_i])
	if s == n:
		break
	if s < n:
		to_i += 1
	else:
		from_i += 1

print(min(nums[from_i:to_i]) + max(nums[from_i:to_i]))
