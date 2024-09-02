#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split()))

numbers = next(load_data('input.txt'))

# Part One

class Node:

	def __init__(self, body):
		self.children = []
		self.metadata = []
		self.size = 2
		n_children = body[0]
		n_metadata = body[1]
		body = body[2:]
		for _ in range(n_children):
			child = Node(body)
			self.size += child.size
			self.children.append(child)
			body = body[child.size:]
		self.metadata = body[:n_metadata]
		self.size += n_metadata

	def sum_metadata(self):
		return sum(self.metadata) + sum(c.sum_metadata() for c in self.children)

	def value(self):
		if len(self.children) == 0:
			return sum(self.metadata)
		return sum( self.children[n-1].value() for n in self.metadata if 0 < n <= len(self.children) )

	def __repr__(self):
		return f"Node({self.children}, {self.metadata})"

root = Node(numbers)

print(root.sum_metadata())

# Part Two

print(root.value())

