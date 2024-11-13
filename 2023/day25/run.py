#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(': ')
			yield t[0], t[1].split()

# Part One

import networkx as nx

g = nx.Graph()

for head, l in load_data('input.txt'):
	for endpoint in l:
		g.add_edge(head, endpoint)

min_cut_edges = nx.minimum_edge_cut(g)

g.remove_edges_from(min_cut_edges)

group_sizes = [len(component) for component in nx.connected_components(g)]

print(group_sizes[0] * group_sizes[1])
