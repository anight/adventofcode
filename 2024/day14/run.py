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

quarts = {}
for p, v in data:
	p += 100 * v
	p = p.real % w + 1j * (p.imag % h)
	if p.real == w // 2 or p.imag == h // 2:
		continue
	key = p.real // (w//2+1) + 1j * (p.imag // (h//2+1))
	quarts[key] = quarts.get(key, 0) + 1

result = 1
for v in quarts.values():
	result *= v

print(result)

# Part Two

# Found this with my eyes, I swear

result = 7858
'''
a = set()
for p, v in data:
	p += result * v
	p = p.real % w + 1j * (p.imag % h)
	a.add(p)
for y in range(h):
	for x in range(w):
		print('@' if x + 1j * y in a else '.', end='')
	print()
'''
print(result)
