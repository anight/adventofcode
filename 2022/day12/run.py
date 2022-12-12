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

from dijkstra import Graph, dijkstra

def from_S_to_E(heightmap, S, E):
	h, w = heightmap.shape

	def get_neighbours(current):
		x, y = current % w, current // w
		height = heightmap[y,x]
		if x > 0 and heightmap[y,x-1] - height <= 1:
			yield current-1, 1
		if x < w-1 and heightmap[y,x+1] - height <= 1:
			yield current+1, 1
		if y > 0 and heightmap[y-1,x] - height <= 1:
			yield current-w, 1
		if y < h-1 and heightmap[y+1,x] - height <= 1:
			yield current+w, 1

	g = Graph(w * h, get_neighbours)

	D = dijkstra(g, S[0] + w * S[1])

	return D[E[0] + w * E[1]]

print(from_S_to_E(heightmap, S, E))

# Part Two

def from_E_to_a(heightmap, E):
	h, w = heightmap.shape

	def get_neighbours(current):
		x, y = current % w, current // w
		height = heightmap[y,x]
		if x > 0 and heightmap[y,x-1] - height >= -1:
			yield current-1, 1
		if x < w-1 and heightmap[y,x+1] - height >= -1:
			yield current+1, 1
		if y > 0 and heightmap[y-1,x] - height >= -1:
			yield current-w, 1
		if y < h-1 and heightmap[y+1,x] - height >= -1:
			yield current+w, 1

	g = Graph(w * h, get_neighbours)

	D = dijkstra(g, E[0] + w * E[1])

	best = None
	for y in range(h):
		for x in range(w):
			if heightmap[y,x] == 0:
				if best is None or D[best[1] + w * best[0]] > D[x + w * y]:
					best = (y, x)

	return D[best[1] + w * best[0]]

print(from_E_to_a(heightmap, E))
