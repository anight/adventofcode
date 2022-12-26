#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

# Part One

lines = list(load_data('input.txt'))

w, h = len(lines[0]), len(lines)
max_minutes = 400
start = 1
end = (h - 1) * w + (w - 2)

from dijkstra import Graph, dijkstra

def get_neighbours(current):
	x, y, t = current % w, (current // w) % h, current // (w * h)
	possible_moves = (
		(x-1, y,   t+1),
		(x+1, y,   t+1),
		(x,   y-1, t+1),
		(x,   y+1, t+1),
		(x,   y,   t+1),
	)
	def can_walk(x, y, t):
		if lines[y][x] == '#':
			return False
		if lines[y][1 + (x - 1 + t) % (w - 2)] == '<':
			return False
		if lines[y][1 + (w - 2 + x - 1 - t % (w - 2)) % (w - 2)] == '>':
			return False
		if lines[1 + (y - 1 + t) % (h - 2)][x] == '^':
			return False
		if lines[1 + (h - 2 + y - 1 - t % (h - 2)) % (h - 2)][x] == 'v':
			return False
		return True
	for (nx, ny, nt) in possible_moves:
		if nx >= 0 and nx < w and ny >= 0 and ny < h and nt < max_minutes:
			if can_walk(nx, ny, nt):
				yield nx + ny * w + nt * w * h, 1

def find_earliest_target(target):
	for t in range(max_minutes):
		if D[t * w * h + target] != float('inf'):
			return t

g = Graph(w * h * max_minutes, get_neighbours)
D = dijkstra(g, start)

t0 = find_earliest_target(end)

print(t0)

# Part Two

max_minutes *= 2

g = Graph(w * h * max_minutes, get_neighbours)
D = dijkstra(g, t0 * w * h + end)

t1 = find_earliest_target(start)

max_minutes += max_minutes // 2

g = Graph(w * h * max_minutes, get_neighbours)
D = dijkstra(g, t1 * w * h + start)

t2 = find_earliest_target(end)

print(t2)
