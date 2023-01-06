#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		S, E = None, None
		for y, line in enumerate(f):
			line = line.rstrip()
			if 'E' in line:
				E = (line.find('E'), y)
				line = line.replace('E', 'z')
			if 'S' in line:
				S = (line.find('S'), y)
				line = line.replace('S', 'a')
			a.append(list(map(lambda c: ord(c) - ord('a'), line)))
		return np.array(a, dtype=int), S, E

import numpy as np

# Part One

heightmap, S, E = load_data('input.txt')

from dijkstra import Graph

def from_S_to_E(heightmap, S, E):
	h, w = heightmap.shape

	class from_S_to_E(Graph):

		@staticmethod
		def neighbours(current):
			x, y = current
			height = heightmap[y,x]
			if x > 0 and heightmap[y,x-1] - height <= 1:
				yield (x-1, y), 1
			if x < w-1 and heightmap[y,x+1] - height <= 1:
				yield (x+1, y), 1
			if y > 0 and heightmap[y-1,x] - height <= 1:
				yield (x, y-1), 1
			if y < h-1 and heightmap[y+1,x] - height <= 1:
				yield (x, y+1), 1

	D = from_S_to_E().dijkstra(S)
	return D[E]

print(from_S_to_E(heightmap, S, E))

# Part Two

def from_E_to_a(heightmap, E):
	h, w = heightmap.shape

	class from_E_to_a(Graph):

		@staticmethod
		def neighbours(current):
			x, y = current
			height = heightmap[y,x]
			if x > 0 and heightmap[y,x-1] - height >= -1:
				yield (x-1, y), 1
			if x < w-1 and heightmap[y,x+1] - height >= -1:
				yield (x+1, y), 1
			if y > 0 and heightmap[y-1,x] - height >= -1:
				yield (x, y-1), 1
			if y < h-1 and heightmap[y+1,x] - height >= -1:
				yield (x, y+1), 1

	D = from_E_to_a().dijkstra(E)

	best = None
	for y in range(h):
		for x in range(w):
			if heightmap[y,x] == 0 and (x, y) in D:
				if best is None or D[best] > D[(x, y)]:
					best = (x, y)

	return D[best]

print(from_E_to_a(heightmap, E))
