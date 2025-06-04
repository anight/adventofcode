#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' <-> ')
			yield int(t[0]), tuple(map(int, t[1].split(', ')))

# Part One

import networkx as nx

G = nx.Graph()

for a, nodes in load_data('input.txt'):
	for node in nodes:
		G.add_edge(a, node)

cc = list(nx.connected_components(G))

for group in cc:
	if 0 in group:
		break

print(len(group))

# Part Two

print(len(cc))

