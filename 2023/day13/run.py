#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		m = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				yield m
				m = []
			else:
				m.append( list(line) )
		yield m

# Part One

import numpy as np
maps = [ np.array(item) for item in load_data('input.txt') ]

total_v, total_h = 0, 0

for m in maps:
	h_line, v_line = None, None
	for h in range(1, m.shape[0]//2+1):
		if np.all(m[:h,...] == m[2*h-1:h-1:-1,...]):
			h_line = h
			break
		elif np.all(m[-h:,...] == m[-h-1:-2*h-1:-1,...]):
			h_line = m.shape[0] - h
			break
	for v in range(1, m.shape[1]//2+1):
		if np.all(m[...,:v] == m[...,2*v-1:v-1:-1]):
			v_line = v
			break
		elif np.all(m[...,-v:] == m[...,-v-1:-2*v-1:-1]):
			v_line = m.shape[1] - v
			break
	assert (v_line is None) != (h_line is None)
	if v_line is not None:
		total_v += v_line
	if h_line is not None:
		total_h += h_line

print(total_v + 100 * total_h)

# Part Two

total_v, total_h = 0, 0

for m in maps:
	h_line, v_line = None, None
	for h in range(1, m.shape[0]//2+1):
		if 1 == np.sum(m[:h,...] != m[2*h-1:h-1:-1,...]):
			h_line = h
			break
		elif 1 == np.sum(m[-h:,...] != m[-h-1:-2*h-1:-1,...]):
			h_line = m.shape[0] - h
			break
	for v in range(1, m.shape[1]//2+1):
		if 1 == np.sum(m[...,:v] != m[...,2*v-1:v-1:-1]):
			v_line = v
			break
		elif 1 == np.sum(m[...,-v:] != m[...,-v-1:-2*v-1:-1]):
			v_line = m.shape[1] - v
			break
	assert (v_line is None) != (h_line is None)
	if v_line is not None:
		total_v += v_line
	if h_line is not None:
		total_h += h_line

print(total_v + 100 * total_h)
