#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split()))

import numpy as np
from itertools import pairwise

# Part One

def extrapolate(nums):
	a = [ nums ]
	while True:
		a.append( np.array([ b - a for a, b in pairwise(a[-1]) ], dtype=int) )
		if np.all(a[-1] == 0):
			break
	left, right = 0, 0
	for i in range(len(a)-2, -1, -1):
		right += a[i][-1]
		left = a[i][0] - left
	return left, right

total = sum( extrapolate(np.array(nums, dtype=int))[1] for nums in load_data('input.txt') )

print(total)

# Part Two

total = sum( extrapolate(np.array(nums, dtype=int))[0] for nums in load_data('input.txt') )

print(total)

