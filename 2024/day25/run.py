#! /usr/bin/env python3

def load_data(filename):
	result = []
	lines = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				continue
			lines.append(list(line))
			if len(lines) == 7:
				result.append(lines)
				lines = []
	return result

import numpy as np
data = np.array(load_data('input.txt'))

# Part One

locks = data[np.where(np.all(data[:,0,:] == '#' , axis=1))]
keys = data[np.where(np.all(data[:,0,:] == '.' , axis=1))]

locks = np.sum(locks == '#', axis=1) - 1
keys = np.sum(keys == '#', axis=1) - 1

result = sum(np.sum(np.all(key + locks <= 5, axis=1)) for key in keys)

print(result)
