#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		match = re.match(r'^(?P<players>\d+) players; last marble is worth (?P<points>\d+) points$', line)
		return int(match.group('players')), int(match.group('points'))

import re

# Part One

players, points = load_data('input.txt')

class State:
	def __init__(self, n_players):
		self.current_player = 0
		self.n_players = n_players
		self.marbles = [0]
		self.current = 0
		self.score = [0] * n_players

	def move(self, marble_id):
		if marble_id % 23 == 0:
			self.score[self.current_player] += marble_id
			i = (self.current - 7) % len(self.marbles)
			self.score[self.current_player] += self.marbles.pop(i)
		else:
			i = (self.current + 2) % len(self.marbles)
			self.marbles.insert(i, marble_id)
		self.current = i
		self.current_player = (self.current_player + 1) % self.n_players

	def play(self, last_marble_id):
		for marble_id in range(1, last_marble_id+1):
			self.move(marble_id)

game = State(players)
game.play(points)

print(max(game.score))

# Part Two

class Node:
	def __init__(self, id):
		self.id = id
		self.next, self.prev = self, self

	def remove(self):
		self.prev.next, self.next.prev = self.next, self.prev
		self.next, self.pref = self, self

	def insert(self, node):
		node.prev, node.next = self.prev, self
		self.prev.next, self.prev = node, node

class FastState(State):
	def __init__(self, n_players):
		super(FastState, self).__init__(n_players)
		self.current = Node(0)

	def move(self, marble_id):
		if marble_id % 23 == 0:
			self.score[self.current_player] += marble_id
			node = self.current.prev.prev.prev.prev.prev.prev.prev
			self.score[self.current_player] += node.id
			self.current = node.next
			node.remove()
		else:
			node = Node(marble_id)
			self.current.next.next.insert(node)
			self.current = node
		self.current_player = (self.current_player + 1) % self.n_players

game = FastState(players)
game.play(points * 100)

print(max(game.score))
