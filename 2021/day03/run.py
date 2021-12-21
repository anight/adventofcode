#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield list(map(int, line))

# Part One

import numpy as np

data = np.array(list(load_data('input.txt')), dtype=int)

gamma = (np.sum(data == 1, axis=0) > np.sum(data == 0, axis=0)).astype(int)

epsilon = 1 - gamma

def array2bin(a):
	return int(''.join(map(str, a)), base=2)

print(array2bin(gamma) * array2bin(epsilon))

# Part Two

def find_number(bit_criteria):
	bit_no = 0
	candidates = np.copy(data)
	while len(candidates) > 1:
		candidates = candidates[np.where(bit_criteria(candidates[:,bit_no]))]
		bit_no += 1
	assert len(candidates) == 1
	return candidates[0]

oxygen = find_number(lambda a: a if np.sum(a == 1) >= np.sum(a == 0) else 1 - a)

co2 = find_number(lambda a: 1 - a if np.sum(a == 1) >= np.sum(a == 0) else a)

print(array2bin(oxygen) * array2bin(co2))
