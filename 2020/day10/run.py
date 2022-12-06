#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield int(line)

# Part One

nums = sorted(load_data('input.txt'))
nums.insert(0, 0)
nums.append(nums[-1] + 3)

from itertools import pairwise

def distances(nums):
	result = {1: 0, 2: 0, 3: 0}
	for a, b in pairwise(nums):
		if b - a > 3:
			return None
		result[b - a] += 1
	return result

result = distances(nums)
print(result[1] * result[3])

# Part Two

def all_ranges():
	start = None
	for i in range(1, len(nums)-1):
		soft = nums[i+1] - nums[i-1] <= 3
		if start is None:
			if soft:
				start = i
		else:
			if not soft:
				yield start, i
				start = None

from itertools import product

total = 1
for from_i, to_i in all_ranges():
	sequence = nums[from_i-1:to_i+1]
	combinations = 0
	for bits in product((0, 1), repeat=to_i-from_i):
		copy = sequence.copy()
		for bit_i, bit in enumerate(bits):
			if bit:
				copy.pop(to_i-from_i-bit_i)
		if distances(copy) is not None:
			combinations += 1
	total *= combinations

print(total)
