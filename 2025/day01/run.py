#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line[0], int(line[1:])

# Part One

total = 0
p = 50
for d, n in load_data('input.txt'):
	if d == 'L':
		n = -n
	p = (p + n) % 100
	if p == 0:
		total += 1

print(total)

# Part Two

total = 0
p = 50
for d, n in load_data('input.txt'):
	step = 1
	if d == 'L':
		step = -1
	while n > 0:
		p = (p + step) % 100
		if p == 0:
			total += 1
		n -= 1

print(total)
