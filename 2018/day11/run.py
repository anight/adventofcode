#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return int(line)

num = load_data('input.txt')

# Part One

import numpy as np

x, y = np.meshgrid(np.arange(1, 301), np.arange(1, 301))
rack_id = x + 10
power_level_starts = rack_id * y
increased_power_level = power_level_starts + num
set_power_level = increased_power_level * rack_id
hundreds = (set_power_level % 1000) // 100
level = hundreds - 5

def max_square(sq):
	swv = np.lib.stride_tricks.sliding_window_view(level, [sq, sq])
	sums = np.sum(swv, axis=(2, 3))
	ind = np.unravel_index(np.argmax(sums), sums.shape)
	return sums[ind[0],ind[1]], ind[1]+1, ind[0]+1

_, x, y = max_square(3)

print(f"{x},{y}")

# Part Two

all_squares = [ max_square(sq) for sq in range(1, 50) ]
m = max(all_squares)
sq = all_squares.index(m)

print(f"{m[1]},{m[2]},{sq+1}")
