#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

office_designer_s_favorite_number = int(next(load_data('input.txt')))

def is_wall(x, y):
	global office_designer_s_favorite_number
	n = x*x + 3*x + 2*x*y + y + y*y
	n += office_designer_s_favorite_number
	return n.bit_count() & 1

import networkx as nx

G = nx.Graph()

s = (1, 1)
e = (31, 39)

for y in range(50):
	for x in range(50):
		if is_wall(x, y):
			continue
		if not is_wall(x+1, y):
			G.add_edge( (x, y), (x+1, y), weight=1 )
		if not is_wall(x, y+1):
			G.add_edge( (x, y), (x, y+1), weight=1 )

result = len(nx.shortest_path(G, s, e)) - 1

print(result)

# Part Two

lengths = nx.single_source_dijkstra_path_length(G, s, cutoff=50, weight='weight')

result = len(lengths)

print(result)

