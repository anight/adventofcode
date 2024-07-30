#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			id, t = line.split(' @ ')
			offset, size = t.split(': ')
			offset = offset.split(',')
			size = size.split('x')
			yield int(id[1:]), int(offset[0]), int(offset[1]), int(size[0]), int(size[1])

import numpy as np

# Part One

a = np.zeros((1000, 1000), dtype=int)

for _, ox, oy, sx, sy in load_data('input.txt'):
	a[oy:oy+sy,ox:ox+sx] += 1

print(np.sum(a > 1))

# Part Two

for claim_id, ox, oy, sx, sy in load_data('input.txt'):
	if np.all(a[oy:oy+sy,ox:ox+sx] == 1):
		break

print(claim_id)
