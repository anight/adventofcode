#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

import networkx as nx
from itertools import pairwise

a = list(load_data('input.txt'))

start = (0, 1)
end = (len(a)-1, len(a[0])-2)

# Part One

def graph(a):
	g = nx.DiGraph()

	for y in range(len(a)-1):
		for x in range(len(a[0])-1):
			if a[y][x] == '.':
				if a[y+1][x] == '.':
					g.add_edge( (y, x), (y+1, x), weight=1 )
					g.add_edge( (y+1, x), (y, x), weight=1 )
				if a[y][x+1] == '.':
					g.add_edge( (y, x), (y, x+1), weight=1 )
					g.add_edge( (y, x+1), (y, x), weight=1 )
			elif a[y][x] == '<':
				g.add_edge( (y, x+1), (y, x), weight=1 )
				g.add_edge( (y, x), (y, x-1), weight=1 )
			elif a[y][x] == '>':
				g.add_edge( (y, x-1), (y, x), weight=1 )
				g.add_edge( (y, x), (y, x+1), weight=1 )
			elif a[y][x] == '^':
				g.add_edge( (y+1, x), (y, x), weight=1 )
				g.add_edge( (y, x), (y-1, x), weight=1 )
			elif a[y][x] == 'v':
				g.add_edge( (y-1, x), (y, x), weight=1 )
				g.add_edge( (y, x), (y+1, x), weight=1 )

	return g

def simplify_graph(graph):
	G_simplified = graph.copy()

	while True:
		for node in list(G_simplified.nodes):
			if graph.is_directed():
				predecessors = list(G_simplified.predecessors(node))
				successors = list(G_simplified.successors(node))
				neighbors = list(set(predecessors + successors))
			else:
				neighbors = list(G_simplified.neighbors(node))

			if len(neighbors) != 2:
				continue

			u, v = neighbors

			if node in G_simplified[u] and v in G_simplified[node]:
				weight_uv = G_simplified[u][node]['weight'] + G_simplified[node][v]['weight']
				G_simplified.add_edge(u, v, weight=weight_uv)
			if node in G_simplified[v] and u in G_simplified[node]:
				weight_uv = G_simplified[v][node]['weight'] + G_simplified[node][u]['weight']
				G_simplified.add_edge(v, u, weight=weight_uv)
			G_simplified.remove_node(node)
			break
		else:
			break
	
	return G_simplified

g = graph(a)

g = simplify_graph(g)

max_weight = 0

for p in nx.all_simple_paths(g, start, end):
	w = sum( g[a][b]['weight'] for a, b in pairwise(p) )
	max_weight = max(max_weight, w)

print(max_weight)


# Part Two

g = graph( [ s.replace('<', '.').replace('>', '.').replace('v', '.').replace('^', '.') for s in a ] )

g = simplify_graph(g)

g = g.to_undirected()

# Thanks, ChatGPT: Depth-limited DFS function for undirected graphs
def depth_limited_dfs(graph, start, end, depth_limit):
	# Initialize variables to store the longest path and its weight
	longest_path = []
	max_weight = float('-inf')

	# Helper function for recursive DFS with depth limit
	def dfs(node, current_path, current_weight, depth, visited):
		nonlocal longest_path, max_weight

		# If we reach the target node and have a longer path, update the result
		if node == end and current_weight > max_weight:
			longest_path = current_path[:]
			max_weight = current_weight
			return

		# If we reach the depth limit, stop exploring further
		if depth == 0:
			return

		# Mark the current node as visited
		visited.add(node)

		# Explore neighbors
		for neighbor in graph.neighbors(node):
			if neighbor not in visited:  # Avoid cycles by not revisiting nodes
				edge_weight = graph[node][neighbor]['weight']
				# Recur with the neighbor node
				dfs(neighbor, current_path + [neighbor], current_weight + edge_weight, depth - 1, visited)

		# Unmark the current node to allow other paths to use it
		visited.remove(node)

	# Start DFS from the start node with the specified depth limit
	dfs(start, [start], 0, depth_limit, set())

	return longest_path, max_weight

path, weight = depth_limited_dfs(g, start, end, 34)

print(weight)

