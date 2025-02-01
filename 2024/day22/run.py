#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

data = list(map(int, load_data('input.txt')))

# Part One

def next_number(n):
	n = ((n << 6) ^ n) & 16777215
	n = ((n >> 5) ^ n) & 16777215
	n = ((n << 11) ^ n) & 16777215
	return n

def cycle(n, num):
	for _ in range(num):
		n = next_number(n)
	return n

result = sum( cycle(n, 2000) for n in data )

print(result)

# Part Two

seq = {}

for i, n in enumerate(data):
	last = n % 10
	s = []
	for _ in range(2000):
		n = next_number(n)
		digit = n % 10
		delta = digit - last
		if len(s) == 4:
			s.pop(0)
		s.append(delta)
		if len(s) < 4:
			continue
		key = tuple(s)
		if key not in seq:
			seq[key] = [None] * len(data)
		if seq[key][i] is None:
			seq[key][i] = digit
		last = digit

result = max(map(lambda v: sum( value if value is not None else 0 for value in v ), seq.values()))

print(result)

