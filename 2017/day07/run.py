#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' -> ')
			name, weight = t[0].split(' ')
			weight = int(weight[1:-1])
			if len(t) > 1:
				nodes = t[1].split(', ')
			else:
				nodes = []
			yield name, weight, nodes

# Part One

all_nodes = {}
children = set()

for name, weight, nodes in load_data('input.txt'):
	all_nodes[name] = (weight, nodes)
	children |= set(nodes)

root = next(iter(set(all_nodes.keys()) - children))

print(root)

# Part Two

from collections import Counter

def tree_weight(node):
	return all_nodes[node][0] + sum( tree_weight(child) for child in all_nodes[node][1] )

delta = None

while True:
	branches = { child: tree_weight(child) for child in all_nodes[root][1] }
	if len(set(branches.values())) == 1:
		break
	normal_weight = Counter(branches.values()).most_common(1)[0][0]
	unbalanced_node, unbalanced_weight = [ (k, v) for k, v in branches.items() if v != normal_weight ][0]
	if delta is None:
		delta = normal_weight - unbalanced_weight
	root = unbalanced_node

print(all_nodes[root][0] + delta)

