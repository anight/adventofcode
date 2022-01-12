#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.strip()
			a.append(list(map(int, line.replace('v', '2').replace('>', '1').replace('.', '0'))))
		return np.array(a, dtype=int)

# Part One

import numpy as np

state = load_data('input.txt')

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=np.int) - np.array(window.shape, dtype=np.int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def onestep(state):

	new = np.pad(state, ((0, 1),), mode='wrap')
	east_kernel = np.array([[1, 0], [-1, -1]], dtype=int)
	rolled = rolling_window(new, east_kernel)
	east_res = np.where(np.sum((rolled == east_kernel), axis=(2, 3)) == 2)
	new[east_res] = 0
	east_res = (east_res[0], (1 + east_res[1]) % state.shape[1])
	new[east_res] = 1

	new = new[:-1,:-1]

	new = np.pad(new, ((0, 1),), mode='wrap')
	south_kernel = np.array([[2, -1], [0, -1]], dtype=int)
	rolled = rolling_window(new, south_kernel)
	south_res = np.where(np.sum(rolled == south_kernel, axis=(2, 3)) == 2)
	new[south_res] = 0
	south_res = ((1 + south_res[0]) % state.shape[0], south_res[1])
	new[south_res] = 2

	return new[:-1,:-1]

step = 0

while True:
	step += 1
	next_state = onestep(state)
	if np.all(next_state == state):
		break
	state = next_state

print(step)

# Part Two

