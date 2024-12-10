#! /usr/bin/env python3

a = { x+1j*y: int(c) for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }
g = lambda c: a.get(c, "")

# Part One

result = 0

for c, zero in a.items():
	if zero != 0:
		continue
	nines = set()
	def reach(c, v):
		if v == 9:
			global nines
			nines.add(c)
			return
		for d in range(4):
			n = c + 1j ** d
			if g(n) == v + 1:
				reach(n, v + 1)
	reach(c, 0)
	result += len(nines)

print(result)

# Part Two

result = 0

for c, zero in a.items():
	if zero != 0:
		continue
	trails = 0
	def reach(c, v):
		if v == 9:
			global trails
			trails += 1
			return
		for d in range(4):
			n = c + 1j ** d
			if g(n) == v + 1:
				reach(n, v + 1)
	reach(c, 0)
	result += trails

print(result)
