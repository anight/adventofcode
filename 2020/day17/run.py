#! /usr/bin/env python3

import numpy as np

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.strip()
			line = line.replace('#', '1').replace('.', '0')
			a.append(list(map(int, line)))
	return np.array(a, dtype=int)

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def next_state_3d(state):
	padded = np.pad(state, 2, mode='constant')
	kernel_neighbours = np.ones( (3,3,3), dtype=int)
	kernel_neighbours[1,1,1] = 0
	rolled = rolling_window(padded, kernel_neighbours)
	current = padded[1:-1,1:-1,1:-1]
	neighbours = np.sum(np.multiply(rolled, kernel_neighbours), axis=(3,4,5))
	return np.logical_or(np.logical_and(current == 1, np.logical_or(neighbours == 2, neighbours == 3)), \
		np.logical_and(current == 0, neighbours == 3)).astype(int)

def next_state_4d(state):
	padded = np.pad(state, 2, mode='constant')
	kernel_neighbours = np.ones( (3,3,3,3), dtype=int)
	kernel_neighbours[1,1,1,1] = 0
	rolled = rolling_window(padded, kernel_neighbours)
	current = padded[1:-1,1:-1,1:-1,1:-1]
	neighbours = np.sum(np.multiply(rolled, kernel_neighbours), axis=(4,5,6,7))
	return np.logical_or(np.logical_and(current == 1, np.logical_or(neighbours == 2, neighbours == 3)), \
		np.logical_and(current == 0, neighbours == 3)).astype(int)

# Part One

state = load_data('input.txt')

# add "z" dimension
state = np.reshape(state, (1,) + state.shape)

for _ in range(6):
	state = next_state_3d(state)

print(np.sum(state))

# Part Two

state = load_data('input.txt')

# add "w", "z" dimensions
state = np.reshape(state, (1,1,) + state.shape)

for _ in range(6):
	state = next_state_4d(state)

print(np.sum(state))
