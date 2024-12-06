#! /usr/bin/env python3

a = { x+1j*y: c for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }
g = lambda c: a.get(c, "")

# Part One

p = next( key for key, value in a.items() if value == '^' )
d = -1j

visited = set()

while True:
	visited.add(p)
	f = p + d
	if g(f) == '':
		break
	if g(f) == '#':
		d *= 1j
	else:
		p = f

print(len(visited))

# Part Two

def walk_is_cycled(p, d, trail, obstacles, try_obstacle=None):
	while True:
		if (p, d) in trail:
			return True
		trail.add((p, d))
		f = p + d
		if g(f) == '':
			return False
		if g(f) == '#' or f == try_obstacle:
			d *= 1j
		else:
			if try_obstacle is None and f not in obstacles:
				# We are about to step forward. What if there was an obstacle instead?
				obstacles[f] = walk_is_cycled(p, d*1j, trail.copy(), obstacles, try_obstacle=f)
			p = f

p = next( key for key, value in a.items() if value == '^' )
d = -1j

# The new obstruction can't be placed at the guard's starting position
obstacles = { p: False }

walk_is_cycled(p, d, set(), obstacles)

print(sum(obstacles.values()))
