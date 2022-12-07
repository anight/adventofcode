#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.strip()
			a.append(list(map(int, line)))
		return np.array(a, dtype=int)

# Part One

import numpy as np

data = load_data('input.txt')

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def oneday(data):
	padded = np.pad(data, 1, 'constant')
	padded[1:-1,1:-1] += 1
	flashes = np.zeros(padded.shape, dtype=int)
	while True:
		new_flashes = np.logical_and(padded > 9, flashes == 0).astype(int)
		if np.sum(new_flashes) == 0:
			break
		flashes += new_flashes
		kernel_neighbours = np.array([[1,1,1],[1,0,1],[1,1,1]], dtype=int)
		rolled = rolling_window(new_flashes, kernel_neighbours)
		add = np.sum(np.multiply(rolled, kernel_neighbours), axis=(2,3))
		padded[1:-1,1:-1] += add
	flashes = np.where(padded > 9)
	padded[flashes] = 0
	data[...] = padded[1:-1,1:-1]
	return len(flashes[0])

flashes = 0

for _ in range(100):
	flashes += oneday(data)

print(flashes)

# Part Two

data = load_data('input.txt')

step = 0

while True:
	step += 1
	oneday(data)
	if np.sum(data) == 0:
		break

print(step)

