#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield list(line.rstrip('\n'))

# Part One

import numpy as np
a = np.array(list(load_data('input.txt')))
a = np.pad(a, 1, 'constant', constant_values='.')

total = 0

numbers = {}

for y, x in zip(*np.where(a >= '0')):
	if a[y, x-1].isdigit():
		numbers[(x, y)] = n
		continue
	n = 0
	non_dots = 0
	key = (x, y)
	while a[y, x].isdigit():
		non_dots += len(set(a[y-1:y+2,x-1:x+2].reshape(-1)) - set('0123456789.'))
		n *= 10
		n += int(a[y, x])
		x += 1

	numbers[key] = n

	if non_dots:
		total += n

print(total)

# Part Two

total = 0

for y, x in zip(*np.where(a == '*')):
	nums = set([ numbers.get((x+dx, y+dy), 0) for dy in range(-1, 2) for dx in range(-1, 2) ])
	if len(nums) == 3:
		nums = list(nums - set([0]))
		total += nums[0] * nums[1]

print(total)
