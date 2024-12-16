#! /usr/bin/env python3

a = { x+1j*y: c for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }

# Part One

from heapq import heappop, heappush
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any
from functools import reduce

def neighbours(c):
	for d in range(4):
		n = c + 1j ** d
		if a.get(n, '*') in '.SE':
			yield n

start = next( c for c, v in a.items() if v == 'S' )
end = next( c for c, v in a.items() if v == 'E' )
direction = 1

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	fields: Any=field(compare=False)

def edge_weight(u, v, prev_direction):
	direction = v - u
	if prev_direction == direction:
		return 1, direction
	return 1001, direction

def dijkstra_best_score(source, target, direction):
	queue = [PrioritizedItem(0, (source, direction))]
	visited = defaultdict(lambda: float('inf'))

	while queue:
		item = heappop(queue)
		cost, current, direction = item.priority, *item.fields
		if current == target:
			return cost
		
		if visited[current] <= cost:
			continue
		
		visited[current] = cost
		
		for neighbour in neighbours(current):
			move_cost, new_direction = edge_weight(current, neighbour, direction)
			new_cost = cost + move_cost
			heappush(queue, PrioritizedItem(new_cost, (neighbour, new_direction)))

result = dijkstra_best_score(start, end, direction)

print(result)


# Part Two

@dataclass
class CostWithHistory:
	cost: float = field(default_factory=lambda: float('inf'))
	history: set = field(default_factory=set)

	def update(self, cost, prev):
		if cost < self.cost:
			self.cost = cost
			self.history = set([prev])
		elif cost == self.cost:
			self.history.add(prev)

@dataclass(frozen=True)
class CoordWithDirection:
	coord: complex
	direction: complex

	@classmethod
	def sentinel(cls):
		return cls(None, None)

	def is_sentinel(self):
		return self.coord == None and self.direction == None

def dijkstra_all_best_paths(source, target, direction):
	queue = [PrioritizedItem(0, (CoordWithDirection(source, direction), CoordWithDirection.sentinel()))]
	visited = defaultdict(CostWithHistory)
	best = CostWithHistory()

	while queue:
		item = heappop(queue)
		cost, current, prev = item.priority, *item.fields

		if cost > visited[current].cost:
			continue

		visited[current].update(cost, prev)

		if current.coord == target:
			if cost <= best.cost:
				best.update(cost, current)
			continue

		for neighbour in neighbours(current.coord):
			move_cost, new_direction = edge_weight(current.coord, neighbour, current.direction)
			new_cost = cost + move_cost
			if new_cost <= best.cost:
				new = CoordWithDirection(neighbour, new_direction)
				heappush(queue, PrioritizedItem(new_cost, (new, current)))

	def reconstruct_paths(item):
		nonlocal visited
		ret = []
		for prev in item.history:
			if prev.is_sentinel():
				return [[]]
			prev_paths = reconstruct_paths(visited[prev])
			for path in prev_paths:
				ret.append(path + [prev.coord])
		return ret

	return reconstruct_paths(best)

paths = dijkstra_all_best_paths(start, end, direction)

result = len(reduce(set.union, map(set, paths)))

print(result)
