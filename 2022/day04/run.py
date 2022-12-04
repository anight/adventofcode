#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			range1, range2 = line.split(',')
			from1, to1 = range1.split('-')
			from2, to2 = range2.split('-')
			yield set(range(int(from1), int(to1)+1)), set(range(int(from2), int(to2)+1))

# Part One

total = 0
for set1, set2 in load_data('input.txt'):
	if set1.issubset(set2) or set2.issubset(set1):
		total += 1

print(total)

# Part Two

total = 0
for set1, set2 in load_data('input.txt'):
	if set1.intersection(set2):
		total += 1

print(total)
