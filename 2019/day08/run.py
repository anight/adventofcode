#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		return list(map(int, f.readline().rstrip()))

import numpy as np
a = np.array(load_data('input.txt'))
a = a.reshape((-1, 6, 25))

# Part One

frame_index = np.argmin(np.sum(a == 0, axis=(1, 2)))
print(np.sum(a[frame_index,...] == 1) * np.sum(a[frame_index,...] == 2))

# Part Two

image = a[(np.argmin(a == 2, axis=0), *np.meshgrid(np.arange(6), np.arange(25), indexing='ij'))]
print(np.array2string(image, formatter={'int': lambda x: ' @'[x]}))
