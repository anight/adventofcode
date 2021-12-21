#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.strip()
			a.append(list(map(int, line)))
		return np.array(a, dtype=int)

# Part One

import numpy as np
from dijkstra import Graph, dijkstra

a = load_data('input.txt')

h, w = a.shape

def from_0_to_last(a):
	h, w = a.shape

	def get_neighbours(current):
		x, y = current % w, current // w
		if x > 0:
			yield current-1, a[y,x-1]
		if x < w-1:
			yield current+1, a[y,x+1]
		if y > 0:
			yield current-w, a[y-1,x]
		if y < h-1:
			yield current+w, a[y+1,x]

	g = Graph(w * h, get_neighbours)

	D = dijkstra(g, 0)

	return D[w*h-1]

print(from_0_to_last(a))

# Part Two

mw, mh = 5, 5

addon = np.tile(np.repeat(np.arange(mw, dtype=int), w), (mh*h, 1)) + \
	np.reshape(np.repeat(np.arange(mh, dtype=int), mw*w*h), (mh*h, mw*w))

a = np.tile(a, (mh, mw)) + addon

a = 1 + ((a - 1) % 9)

print(from_0_to_last(a))
