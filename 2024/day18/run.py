#! /usr/bin/env python3

bytes = [ tuple(map(int, line.split(','))) for line in open('input.txt').read().splitlines() ]
limit = 1024
w, h = 71, 71
start, end = (0, 0), (70, 70)

# Part One and Two

import networkx as nx

G = nx.grid_2d_graph(w, h)

for i, pos in enumerate(bytes):
	if i == limit:
		p = nx.shortest_path(G, start, end)
		print(len(p)-1)
	G.remove_node(pos)
	if i >= limit and pos in p:
		try:
			p = nx.shortest_path(G, start, end)
		except nx.exception.NetworkXNoPath:
			break

print(f'{pos[0]},{pos[1]}')
