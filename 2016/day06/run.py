#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

import numpy as np
from collections import Counter

a = np.array(list(load_data('input.txt'))).transpose()

def most_common(lst):
	c = Counter(lst)
	return c.most_common(1)[0][0]

result = ''.join(most_common(column) for column in a )

print(result)

# Part Two

def least_common(lst):
	c = Counter(lst)
	ordered = sorted([ (v, k) for k, v in c.items()])
	return ordered[0][1]

result = ''.join(least_common(column) for column in a )

print(result)
