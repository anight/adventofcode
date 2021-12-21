#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			n = int(line)
			yield n

# Part One

prev_value = None
inc = 0

for value in load_data('input.txt'):
	if prev_value is not None:
		if value > prev_value:
			inc += 1
	prev_value = value

print(inc)

# Part Two

import numpy as np

data = np.array(list(load_data('input.txt')), dtype=int)

summed = np.convolve(data, [1, 1, 1], mode='valid')

diff = np.convolve(summed, [1, -1], mode='valid')

print(np.sum((diff > 0).astype(int)))

