#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		def tonum(s):
			return list(map(int, s.replace('.', '0').replace('#', '1')))
		algo = tonum(f.readline().strip())
		f.readline()
		image = []
		for line in f:
			line = line.strip()
			image.append(tonum(line))
		return np.array(algo, dtype=int), np.array(image, dtype=int)

# Part One

import numpy as np

algo, image = load_data('input.txt')

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def enhance(algo, image, inverted):
	toggle = algo[0]
	kernel = np.array( [ 256 >> i for i in range(9) ], dtype=int ).reshape((3, 3))
	padded = np.pad(image, 2, 'constant')
	rolled = rolling_window(padded, kernel)
	return algo[np.sum(np.multiply(rolled^inverted, kernel), axis=(2,3))]^inverted^toggle, inverted^toggle

inverted = 0

for _ in range(2):
	image, inverted = enhance(algo, image, inverted)

print(np.sum(image))

# Part Two

for _ in range(2, 50):
	image, inverted = enhance(algo, image, inverted)

print(np.sum(image))

