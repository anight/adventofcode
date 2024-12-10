#! /usr/bin/env python3

a = { x+1j*y: int(c) for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }
g = lambda c: a.get(c, "")

# Part One & Two

result1, result2 = 0, 0

for c, zero in a.items():
	if zero != 0:
		continue
	nines = []
	def reach(c, v):
		if v == 9:
			nines.append(c)
			return
		for d in range(4):
			n = c + 1j ** d
			if g(n) == v + 1:
				reach(n, v + 1)
	reach(c, 0)
	result1 += len(set(nines))
	result2 += len(nines)

print(result1, result2, sep='\n')

