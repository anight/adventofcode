#! /usr/bin/env python3

a = { x+1j*y: int(c) for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }

# Part One

from heapq import heappop, heappush
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

start = 0
end = max(a.keys(), key=lambda i: i.real + i.imag)

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	fields: Any=field(compare=False)

@dataclass(frozen=True)
class CoordWithDirectionAndSteps:
	coord: complex
	direction: complex
	steps: int

def dijkstra_best_score(source, target, possible_moves):
	queue = [PrioritizedItem(0, CoordWithDirectionAndSteps(source, 0, 0))]
	visited = defaultdict(lambda: float('inf'))

	while queue:
		item = heappop(queue)
		cost, current = item.priority, item.fields
		if current.coord == target:
			return cost
		
		if visited[current] <= cost:
			continue
		
		visited[current] = cost
		
		for move_cost, neighbour in possible_moves(current):
			new_cost = cost + move_cost
			heappush(queue, PrioritizedItem(new_cost, neighbour))

def possible_moves_part_one(c):
	max_steps = 3
	for d in range(4):
		d = 1j ** d
		n = c.coord + d
		cost = a.get(n, 0)
		if cost != 0:
			if c.steps and c.direction == d:
				yield cost, CoordWithDirectionAndSteps(n, d, c.steps-1)
			elif d in (c.direction * 1j, c.direction * -1j) or c.direction == 0:
				yield cost, CoordWithDirectionAndSteps(n, d, max_steps-1)

result = dijkstra_best_score(start, end, possible_moves_part_one)

print(result)

# Part Two

def possible_moves_part_two(c):
	min_steps = 4
	max_steps = 10
	for d in range(4):
		d = 1j ** d
		n = c.coord + d
		cost = a.get(n, 0)
		if cost != 0:
			if c.steps and c.direction == d:
				yield cost, CoordWithDirectionAndSteps(n, d, c.steps-1)
			elif (c.steps <= max_steps-min_steps and d in (c.direction * 1j, c.direction * -1j)) or c.direction == 0:
				yield cost, CoordWithDirectionAndSteps(n, d, max_steps-1)

result = dijkstra_best_score(start, end, possible_moves_part_two)

print(result)
