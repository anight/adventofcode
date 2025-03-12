#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t1 = line.split(' = ')
			t2 = t1[0].split(' to ')
			yield int(t1[1]), t2[0], t2[1]

# Part One

import itertools
import networkx as nx

G = nx.Graph()

for distance, f, t in load_data('input.txt'):
	G.add_edge(f, t, weight=distance)

def solve_shortest_hamiltonian_path(G):
	nodes = list(G.nodes)
	num_nodes = len(nodes)

	# Brute-force search over all permutations of nodes
	best_path = None
	min_cost = float("inf")

	for perm in itertools.permutations(nodes):  # Try all orderings
		try:
			cost = sum(G[perm[i]][perm[i+1]]['weight'] for i in range(num_nodes - 1))
			if cost < min_cost:
				min_cost = cost
				best_path = perm  # This is the optimal open path
		except KeyError:
			# This catches cases where a path doesn't exist in non-complete graphs
			continue

	return best_path, min_cost

path, cost = solve_shortest_hamiltonian_path(G)

print(cost)

# Part Two

def solve_longest_hamiltonian_path(G):
	nodes = list(G.nodes)
	num_nodes = len(nodes)

	# Brute-force search over all permutations of nodes
	best_path = None
	max_cost = float("-inf")  # Start with negative infinity

	for perm in itertools.permutations(nodes):  # Try all orderings
		try:
			cost = sum(G[perm[i]][perm[i+1]]['weight'] for i in range(num_nodes - 1))
			if cost > max_cost:  # Maximization instead of minimization
				max_cost = cost
				best_path = perm  # Store the best (longest) path
		except KeyError:
			# This catches cases where a path doesn't exist in non-complete graphs
			continue

	return best_path, max_cost

path, cost = solve_longest_hamiltonian_path(G)

print(cost)

