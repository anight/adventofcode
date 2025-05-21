#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			match = re.findall(r' a (?:(\w+)(?:-compatible)? (microchip|generator))(?:\.|,| and)', line)
			yield match

import re
from typing import Callable
from collections import namedtuple
from collections.abc import Iterator
from itertools import combinations
import networkx as nx

type FS = frozenset[str]

FloorNT = namedtuple('FloorNT', ('generators', 'microchips'))

class Floor(FloorNT):
	generators: FS
	microships: FS

	@classmethod
	def empty(cls) -> 'Floor':
		return cls(frozenset(), frozenset())

	@classmethod
	def from_input(cls, items: list[tuple[str, str]]) -> 'Floor':
		microchips = set()
		generators = set()
		for element, type in items:
			if type == 'microchip':
				microchips.add(element)
			elif type == 'generator':
				generators.add(element)
		return cls(frozenset(generators), frozenset(microchips))

	def is_valid(self) -> bool:
		return not self.generators or not (self.microchips - self.generators)

	def to_input(self) -> list[tuple[str, str]]:
		return [ (element, 'generator') for element in self.generators ] + \
			[ (element, 'microchip') for element in self.microchips ]

	def set_op(self, op: Callable[[FS, FS], FS], other: 'Floor') -> 'Floor':
		return Floor(op(self.generators, other.generators), op(self.microchips, other.microchips))

	def __sub__(self, other: 'Floor') -> 'Floor':
		return self.set_op(frozenset.difference, other)

	def __add__(self, other: 'Floor') -> 'Floor':
		return self.set_op(frozenset.union, other)

StateNT = namedtuple('StateNT', ('elevator_floor', 'floors'))

class State(StateNT):

	elevator_floor: int
	floors: tuple['Floor']

	@classmethod
	def from_input(cls, data: list) -> 'State':
		return cls(0, tuple( Floor.from_input(items) for items in data ) )

	@classmethod
	def end(cls, s: 'State') -> 'State':
		full_floor = Floor.empty()
		for floor in s.floors:
			full_floor = full_floor + floor
		assert full_floor.generators == full_floor.microchips
		last_floor = len(s.floors)-1
		return cls(last_floor, tuple( Floor.empty() if i < last_floor else full_floor for i in range(last_floor+1) ))

	def next_states(self) -> Iterator['State']:
		if self.elevator_floor > 0:
			# The elevator can go one floor down
			yield from self.next_states_floor(self.elevator_floor-1)
		if self.elevator_floor < len(self.floors)-1:
			# The elevator can go one floor up
			yield from self.next_states_floor(self.elevator_floor+1)

	def next_states_floor(self, next_floor_n: int) -> Iterator['State']:
		this_floor = self.floors[self.elevator_floor]
		next_floor = self.floors[next_floor_n]

		def try_next_state(next_floor_n, elevator):
			new_this_floor = this_floor - elevator
			new_next_floor = next_floor + elevator
			if new_this_floor.is_valid() and new_next_floor.is_valid():
				# So what
				yield State(next_floor_n, tuple( new_this_floor if floor is this_floor else new_next_floor if floor is next_floor else floor for floor in self.floors ))

		items = this_floor.to_input()

		# Try to pick one item
		for item in items:
			elevator = Floor.from_input([item])
			# Heuristic 1: don't take down microchips
			if next_floor_n < self.elevator_floor and item[1] == 'microchip':
				continue
			yield from try_next_state(next_floor_n, elevator)

		# Heuristic 2: don't take down any pairs
		if next_floor_n < self.elevator_floor:
			return

		# Try all possible pairs
		for item1, item2 in combinations(items, 2):
			elevator = Floor.from_input([item1, item2])
			yield from try_next_state(next_floor_n, elevator)

# Part One

def steps(input):

	start_state = State.from_input(input)
	end_state = State.end(start_state)

	G = nx.Graph()

	to_check = [start_state]
	while to_check:
		state = to_check.pop(-1)
		for new_state in state.next_states():
			if new_state not in G.nodes:
				to_check.append(new_state)
			G.add_edge(state, new_state)

	p = nx.shortest_path(G, start_state, end_state)

	return len(p)-1

input = list(load_data("input.txt"))

print(steps(input))

# Part Two

input[0].extend([
	('elerium', 'generator'),
	('elerium', 'microchip'),
	('dilithium', 'generator'),
	('dilithium', 'microchip'),
])

print(steps(input))

