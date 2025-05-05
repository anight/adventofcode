#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return list(map(int, line.split()))

# Part One

banks = load_data('input.txt')
seen = dict()
steps = 0

while tuple(banks) not in seen:
	seen[tuple(banks)] = steps
	b = max(banks)
	i = banks.index(b)
	banks[i] = 0
	while b > 0:
		i = (i + 1) % len(banks)
		banks[i] += 1
		b -= 1
	steps += 1

print(steps)

# Part One

print(steps - seen[tuple(banks)])
