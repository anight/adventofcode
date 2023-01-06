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
start = (1, 0)
end = (w-2, h-1)

from dijkstra import Graph

class Walker(Graph):

	@staticmethod
	def neighbours(current):
		x, y, t = current
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
					yield (nx, ny, nt), 1

def find_earliest_target(target):
	t = 0
	while True:
		if D.get(target + (t,), float('inf')) != float('inf'):
			return t
		t += 1

D = Walker().dijkstra(start + (0,))
t0 = find_earliest_target(end)

print(t0)

# Part Two

max_minutes *= 2

D = Walker().dijkstra(end + (t0,))
t1 = find_earliest_target(start)

max_minutes += max_minutes // 2

D = Walker().dijkstra(start + (t1,))
t2 = find_earliest_target(end)

print(t2)
