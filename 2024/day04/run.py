#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

import numpy as np

data = list(load_data('input.txt'))
a = np.array(data)

# Part One

def num(k):
	def num(k):
		swv = np.lib.stride_tricks.sliding_window_view(a, k.shape)
		return np.sum(np.all(np.logical_or(swv == k, k == '.'), axis=(2, 3)))
	return sum( num(np.rot90(k, i)) for i in range(4) )

result = num(np.array([[*'XMAS']])) + \
	num(np.array([[*'X...'], [*'.M..'], [*'..A.'], [*'...S']]))

print(result)

# Part Two

result = num(np.array([[*'M.S'], [*'.A.'], [*'M.S']]))

print(result)
