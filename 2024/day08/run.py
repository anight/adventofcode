#! /usr/bin/env python3

a = { x+1j*y: c for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }
g = lambda c: a.get(c, "")

# Part One

from itertools import combinations

all_antennas = set(a.values()) - set(['.'])

def all_pairs():
	for antenna in all_antennas:
		coords = [ key for key, value in a.items() if value == antenna ]
		for n, m in combinations(coords, 2):
			yield m, n

antidots = set()

for m, n in all_pairs():
	d = m - n
	if g(n - d) != '':
		antidots.add(n - d)
	if g(m + d) != '':
		antidots.add(m + d)

print(len(antidots))

# Part Two

antidots = set()

for m, n in all_pairs():
	d = m - n
	antidots |= set( m + k*d for k in range(-100, 100) if g(m + k*d) != '' )

print(len(antidots))
