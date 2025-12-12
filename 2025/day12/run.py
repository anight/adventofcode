#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		figures = []
		areas = []
		fig_nums = []
		figure = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				figures.append(figure)
				figure = []
				continue
			if line[1] == ':':
				continue
			if '#' in line:
				figure.append(tuple(line))
			elif ': ' in line:
				s = line.split(': ')
				size = s[0].split('x')
				areas.append(tuple(map(int, size)))
				fig_nums.append(tuple(map(int, s[1].split())))
		return np.array(figures), np.array(areas), np.array(fig_nums)

# Part One

import numpy as np

figures, areas, fig_nums = load_data('input.txt')

fig_sizes = np.sum(figures == '#', axis=(1,2))

sure_impossible = np.sum(areas[:,0] * areas[:,1] < np.sum(fig_nums * fig_sizes, axis=1))

sure_possible = np.sum((areas[:,0] // 3) * (areas[:,1] // 3) >= np.sum(fig_nums, axis=1))

assert sure_impossible + sure_possible == areas.shape[0]

print(sure_possible)
