#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			x, y = line.split(',')
			yield P(int(x), int(y))

from itertools import combinations
from collections import namedtuple

P = namedtuple('Point', 'x y')

reds = list(load_data('input.txt'))

# Part One

max_area = max( abs(a.x-b.x+1) * abs(a.y-b.y+1) for a, b in combinations(reds, 2) )
print(max_area)

# Part Two

from bisect import bisect_left

sx = sorted( set([p.x for p in reds]) )
sy = sorted( set([p.y for p in reds]) )
w, h = len(sx)+2, len(sy)+2

def tosq(x, y):
	return 1+bisect_left(sx, x), 1+bisect_left(sy, y)

# The field
a = {}

# First draw Red and Green tiles
last = P(*tosq(*reds[-1]))
for c in reds:
	c = P(*tosq(*c))
	a[c] = 'R'
	if last.x == c.x:
		dx = 0
		dy = (c.y-last.y) // abs(c.y-last.y)
	elif last.y == c.y:
		dx = (c.x-last.x) // abs(c.x-last.x)
		dy = 0
	else:
		raise Exception("oops")
	while last != c:
		if last not in a:
			a[last] = 'G'
		last = P(last.x+dx, last.y+dy)

def flood_fill(s, color):
	pool = {s}
	def add(x, y):
		if 0 <= x < w and 0 <= y < h and (x, y) not in a:
			pool.add(P(x, y))
	while pool:
		p = pool.pop()
		a[p] = color
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			add(p.x+dx, p.y+dy)

# Then flood fill with Blue all "outside" tiles
flood_fill( P(0, 0), 'B' )

x, y = next(iter( (x, y) for y in range(h) for x in range(w) if (x, y) not in a ))

# Then flood fill with Green all "inside" tiles
flood_fill( P(x, y), 'G' )

# Make sure all tiles are colored
assert len(a) == w * h

max_area = 0

# Now find the largest rectangle assuming there is no Blue tiles on the borders of the rectangle
for m, n in combinations(reds, 2):
	x1, x2 = sorted([m.x, n.x])
	y1, y2 = sorted([m.y, n.y])
	sx1, sy1 = tosq(x1, y1)
	sx2, sy2 = tosq(x2, y2)
	area = (x2-x1+1) * (y2-y1+1)
	if area < max_area:
		continue
	# Check the borders for Blue tiles
	if any( (a[(x,sy1)] == 'B' or a[(x,sy2)] == 'B') for x in range(sx1, sx2+1) ) or \
		any( (a[(sx1,y)] == 'B' or a[(sx2,y)] == 'B') for y in range(sy1+1, sy2) ):
			continue
	max_area = area

print(max_area)
