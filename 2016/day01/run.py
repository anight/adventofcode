#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		for c in line.split(', '):
			yield c[0], int(c[1:])

# Part One

p, d = 0, -1j

for turn, steps in load_data('input.txt'):
	d *= {'R': -1j, 'L': 1j}[turn]
	p += steps * d

print(int(abs(p.real) + abs(p.imag)))

# Part Two

p, d = 0, -1j
visited = set()

for turn, steps in load_data('input.txt'):
	d *= {'R': -1j, 'L': 1j}[turn]
	for step in range(steps):
		p += d
		if p in visited:
			break
		visited.add(p)
	else:
		continue
	break

print(int(abs(p.real) + abs(p.imag)))
