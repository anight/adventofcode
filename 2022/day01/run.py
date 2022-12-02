#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		nums = []
		for line in f:
			line = line.strip()
			if line == '':
				yield nums
				nums = []
			else:
				nums.append(int(line))
		yield nums

# Part One

sums = sorted([ sum(nums) for nums in load_data('input.txt') ], reverse=True)

print(sums[0])

# Part Two

print(sum(sums[:3]))
