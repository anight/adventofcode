#! /usr/bin/env python3

a = { (x, y): c for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }
least = 100

# Part One

from heapq import heappop, heappush
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

start = next( c for c, v in a.items() if v == 'S' )
end = next( c for c, v in a.items() if v == 'E' )

def neighbours(x, y):
	for dx, dy in [ (1, 0), (-1, 0), (0, 1), (0, -1) ]:
		if a.get( (x+dx, y+dy) ) in '.E':
			yield x+dx, y+dy

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	fields: Any=field(compare=False)

def dijkstra(source):
	queue = [PrioritizedItem(0, source)]
	visited = defaultdict(lambda: float('inf'))

	while queue:
		item = heappop(queue)
		cost, current = item.priority, item.fields
		
		if visited[current] <= cost:
			continue
		
		visited[current] = cost
		
		for neighbour in neighbours(*current):
			new_cost = cost + 1
			heappush(queue, PrioritizedItem(new_cost, neighbour))

	return visited

v = dijkstra(start)

saved = defaultdict(int)

from itertools import combinations

for p1, p2 in combinations(v.keys(), 2):
	x1, y1 = p1
	x2, y2 = p2
	if (x1 == x2 and abs(y1 - y2) == 2 and a.get( (x1, (y1+y2) // 2) ) == '#') or \
		(y1 == y2 and abs(x1 - x2) == 2 and a.get( ((x1+x2) // 2, y1) ) == '#'):
		delta = abs(v[p1] - v[p2]) - 2
		saved[delta] += 1

result = sum( v for k, v in saved.items() if k >= least )

print(result)

# Part Two

saved = defaultdict(int)

for p1, p2 in combinations(v.keys(), 2):
	if v[p1] > v[end] or v[p2] > v[end]:
		continue
	x1, y1 = p1
	x2, y2 = p2
	if abs(x1-x2) + abs(y1-y2) <= 20:
		delta = abs(v[p1] - v[p2]) - (abs(x1-x2) + abs(y1-y2))
		saved[delta] += 1

result = sum( v for k, v in saved.items() if k >= least )

print(result)
