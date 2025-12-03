#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

from itertools import combinations

total = 0

for bank in load_data('input.txt'):
	max_j = 0
	for h, l in combinations(bank, 2):
		max_j = max(max_j, int(h + l))
	total += max_j

print(total)

# Part Two

total = 0

def max_j(bank, n):
	if n == 1:
		return int(max(bank))
	candidates = bank[:1-n]
	m = max(candidates)
	i = candidates.index(m)
	return int(m) * (10 ** (n-1)) + max_j(bank[i+1:], n-1)

for bank in load_data('input.txt'):
	total += max_j(bank, 12)

print(total)
