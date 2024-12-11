#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

import numpy as np

a = np.array(list(load_data('input.txt')))

def trace_light(tracing):

	light = set([])
	while len(tracing):
		new_tracing = set([])
		for x, y, dx, dy in tracing:
			x += dx
			y += dy
			if x < 0 or y < 0 or x >= a.shape[1] or y >= a.shape[0]:
				continue
			if a[y, x] == '\\':
				dx, dy = dy, dx
			elif a[y, x] == '/':
				dx, dy = -dy, -dx
			elif a[y, x] == '|' and dx != 0:
				dx, dy = dy, dx
				new_tracing.add( (x, y, 0, -1) )
				new_tracing.add( (x, y, 0, 1) )
			elif a[y, x] == '-' and dy != 0:
				dx, dy = dy, dx
				new_tracing.add( (x, y, -1, 0) )
				new_tracing.add( (x, y, 1, 0) )
			new_tracing.add( (x, y, dx, dy) )
		new_tracing -= light
		light |= new_tracing
		tracing = new_tracing

	return len(set([ (x, y) for x, y, _, _ in light ]))

ret = trace_light({ (-1, 0, 1, 0) })

print(ret)

# Part Two

max_light = 0

for y in range(a.shape[0]):
	max_light = max(max_light, trace_light({ (-1, y, 1, 0) }))
	max_light = max(max_light, trace_light({ (a.shape[1], y, -1, 0) }))

for x in range(a.shape[1]):
	max_light = max(max_light, trace_light({ (x, -1, 0, 1) }))
	max_light = max(max_light, trace_light({ (x, a.shape[0], 0, -1) }))

print(max_light)
