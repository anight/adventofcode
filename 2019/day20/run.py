#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield list(map(ord, line.rstrip('\n')))

import numpy as np
from itertools import product

field = np.array(list(load_data('input.txt')), dtype=int)
h, w = field.shape

# Part One

teleports = {}
tmp_peers = {}

def found_portal(x, y, dx, dy):
	global w, h

	name = chr(field[y, x]) + chr(field[y+dy, x+dx])
	inner = False

	if dx > 0:
		if x != 0 and x != w-2:
			inner = True
		if x > 0 and field[y, x-1] == ord('.'):
			to_portal = (x-1, y, 1, 0)
		else:
			to_portal = (x+2, y, -1, 0)
	else:
		if y != 0 and y != h-2:
			inner = True
		if y > 0 and field[y-1, x] == ord('.'):
			to_portal = (x, y-1, 0, 1)
		else:
			to_portal = (x, y+2, 0, -1)

	if name in tmp_peers:
		peer_to_portal, peer_inner = tmp_peers[name]
		teleports[(to_portal[0]+to_portal[2], to_portal[1]+to_portal[3])] = \
			((peer_to_portal[0], peer_to_portal[1]), int(inner) - int(peer_inner))
		teleports[(peer_to_portal[0]+peer_to_portal[2], peer_to_portal[1]+peer_to_portal[3])] = \
			((to_portal[0], to_portal[1]), int(peer_inner) - int(inner))
		del tmp_peers[name]
	else:
		tmp_peers[name] = (to_portal, inner)

for y, x in product(range(h), range(w)):
	if ord('A') <= field[y, x] <= ord('Z'):
		if x < w-1 and ord('A') <= field[y, x+1] <= ord('Z'):
			found_portal(x, y, 1, 0)
		elif y < h-1 and ord('A') <= field[y+1, x] <= ord('Z'):
			found_portal(x, y, 0, 1)

assert len(tmp_peers) == 2

start = tmp_peers["AA"][0][:2]
end = tmp_peers["ZZ"][0][:2]

from dijkstra import Graph

def getD(start):

	class Walker(Graph):

		@staticmethod
		def neighbours(current):
			x, y = current
			dx, dy = 1, 0
			for _ in range(4):
				if field[y+dy, x+dx] == ord('.'):
					yield (x+dx, y+dy), 1
				elif (x+dx, y+dy) in teleports:
					yield teleports[(x+dx, y+dy)][0], 1
				dx, dy = -dy, dx

	return Walker().dijkstra(start)

D = getD(start)

print(D[end][0])

# Part Two

max_level = 50

start = tmp_peers["AA"][0][:2] + (0,)
end = tmp_peers["ZZ"][0][:2] + (0,)

def getD(start):

	class Walker(Graph):

		@staticmethod
		def neighbours(current):
			x, y, l = current
			dx, dy = 1, 0
			for _ in range(4):
				if field[y+dy, x+dx] == ord('.'):
					yield (x+dx, y+dy, l), 1
				elif (x+dx, y+dy) in teleports:
					new_coords, delta_level = teleports[(x+dx, y+dy)]
					if 0 <= l + delta_level < max_level:
						yield (new_coords[0], new_coords[1], l+delta_level), 1
				dx, dy = -dy, dx

	return Walker().dijkstra(start)

D = getD(start)

print(D[end][0])
