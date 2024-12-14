#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' ')
			c = lambda token: complex(*list(map(int, token[2:].split(','))))
			yield c(t[0]), c(t[1])

data = list(load_data('input.txt'))

# Part One

w, h = 101, 103

q = {}
for p, v in data:
	p += 100 * v
	p = complex(p.real % w, p.imag % h)
	if p.real == w // 2 or p.imag == h // 2:
		continue
	key = complex(p.real // (w//2+1), p.imag // (h//2+1))
	q[key] = q.get(key, 0) + 1

result = 1
for v in q.values():
	result *= v

print(result)

# Part Two

# Well well well

