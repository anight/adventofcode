#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield tuple(line.split('-'))

data = list(load_data('input.txt'))

# Part One

import networkx as nx

G = nx.Graph()

for n1, n2 in data:
	G.add_edge(n1, n2)

all_cliques = list(nx.enumerate_all_cliques(G))

triangles = [clique for clique in all_cliques if len(clique) == 3 and 't' in clique[0][0]+clique[1][0]+clique[2][0]]

print(len(triangles))

# Part Two

nodes = max( (len(clique), clique) for clique in all_cliques )[1]

print(','.join(sorted(nodes)))
