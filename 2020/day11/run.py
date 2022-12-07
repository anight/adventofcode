#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.rstrip()
			line = line.replace('L', '1').replace('.', '0')
			a.append(list(map(int, line)))
		return a

import numpy as np

# -1: Floor, 0: Free, 1: Occupied
state = np.array(load_data('input.txt'), dtype=int) - 1

# Part One

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def calc_next_state(state):
	padded = np.pad(state, 1, mode='constant')
	kernel_neighbours = np.ones( (3,3), dtype=int)
	kernel_neighbours[1,1] = 0
	rolled = rolling_window((padded == 1).astype(int), kernel_neighbours)
	neighbours = np.sum(np.multiply(rolled, kernel_neighbours), axis=(2,3))
	ret = np.logical_or(np.logical_and(state == 0, neighbours == 0), \
		np.logical_and(state == 1, neighbours < 4)).astype(int)
	ret[np.where(state == -1)] = -1
	return ret

while True:
	new_state = calc_next_state(state)
	if np.all(new_state == state):
		break
	state = new_state

print(np.sum(state == 1))

# Part Two

from itertools import product

state = np.array(load_data('input.txt'), dtype=int) - 1

def calc_neighbours(state, x, y):
	n_neighbours = 0
	for dx, dy in product((-1, 0, 1), repeat=2):
		if (dx, dy) == (0, 0):
			continue
		tx, ty = x, y
		while True:
			tx += dx
			ty += dy
			if tx < 0 or tx >= state.shape[1] or ty < 0 or ty >= state.shape[0]:
				break
			if state[ty][tx] != -1:
				if state[ty][tx] == 1:
					n_neighbours += 1
				break
	return n_neighbours

def calc_next_state2(state):
	new_state = []
	for y in range(state.shape[0]):
		new_line = []
		for x in range(state.shape[1]):
			if state[y][x] == -1:
				new_value = -1
			else:
				n_neighbours = calc_neighbours(state, x, y)
				if state[y][x] == 0 and n_neighbours == 0:
					new_value = 1
				elif state[y][x] == 1 and n_neighbours >= 5:
					new_value = 0
				else:
					new_value = state[y][x]
			new_line.append(new_value)
		new_state.append(new_line)
	return np.array(new_state, dtype=int)

while True:
	new_state = calc_next_state2(state)
	if np.all(new_state == state):
		break
	state = new_state

print(np.sum(state == 1))

