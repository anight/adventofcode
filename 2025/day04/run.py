#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

import numpy as np
a = np.array(list(load_data('input.txt')))

# Part One

def accessible(a):
	padded = np.pad(a, 1, mode='constant', constant_values='.')
	k = np.array([[*'@@@'], [*'@.@'], [*'@@@']])
	swv = np.lib.stride_tricks.sliding_window_view(padded, k.shape)
	neighbours = np.sum(swv == k, axis=(2, 3))
	return np.logical_and(neighbours < 4, a == '@')

print(np.sum(accessible(a)))

# Part Two

total = 0

while True:
	to_remove = accessible(a)
	if np.sum(to_remove) == 0:
		break
	total += np.sum(to_remove)
	a[np.where(to_remove)] = '.'

print(total)
