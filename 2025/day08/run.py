#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield tuple(map(int, line.split(',')))

from math import dist
from itertools import combinations
import networkx as nx

# Part One

jbs = load_data('input.txt')

distances = [ (dist(a, b), a, b) for a, b in combinations(jbs, 2) ]
distances = sorted(distances)

G = nx.Graph()

for _, a, b in distances[:1000]:
	G.add_edge(a, b)

g = sorted(nx.connected_components(G), key=len, reverse=True)

print(len(g[0]) * len(g[1]) * len(g[2]))

# Part Two

for _, a, b in distances[1000:]:
	G.add_edge(a, b)
	if len(next(nx.connected_components(G))) == 1000:
		break

print(a[0] * b[0])
