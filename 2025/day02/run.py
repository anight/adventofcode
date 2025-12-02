#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			for t in line.split(','):
				yield t.split('-')

# Part One

def is_invalid(n):
	n = str(n)
	k = len(n) // 2
	return n[:k] == n[k:]

total = 0

for f, t in load_data('input.txt'):
	for n in range(int(f), int(t)+1):
		if is_invalid(n):
			total += n

print(total)

# Part Two

def is_invalid(n):
	n = str(n)
	for k in range(1, len(n) // 2 + 1):
		if n == n[:k] * (len(n) // k):
			return True
	return False

total = 0

for f, t in load_data('input.txt'):
	for n in range(int(f), int(t)+1):
		if is_invalid(n):
			total += n

print(total)
