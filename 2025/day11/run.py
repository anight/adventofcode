#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split()
			yield t[0][:-1], t[1:]

# Part One

import networkx as nx

G = nx.DiGraph()

for node, outputs in load_data('input.txt'):
	for o in outputs:
		G.add_edge(node, o)

print(len(list(nx.all_simple_paths(G, 'you', 'out'))))

# Part Two

assert nx.is_directed_acyclic_graph(G)

def n_paths(G, source, target):

    paths = {node: 0 for node in G.nodes()}
    paths[source] = 1

    for node in nx.topological_sort(G):
        for nbr in G.successors(node):
            paths[nbr] += paths[node]

    return paths[target]

result = n_paths(G, 'svr', 'fft') * n_paths(G, 'fft', 'dac') * n_paths(G, 'dac', 'out')

print(result)

