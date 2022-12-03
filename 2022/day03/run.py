#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line

# Part One

def priority(char):
	if char >= 'a' and char <= 'z':
		return ord(char) - ord('a') + 1
	if char >= 'A' and char <= 'Z':
		return ord(char) - ord('A') + 27

total = 0
for line in load_data('input.txt'):
	common = set.intersection(
		set(line[:len(line)//2]),
		set(line[len(line)//2:])
	)
	for char in common:
		total += priority(char)

print(total)

# Part Two

def group_by(it, n):
	lst = list(it)
	for idx in range(0, len(lst), n):
		yield lst[idx:idx+n]

total = 0
for group in group_by(load_data('input.txt'), 3):
	common = set.intersection(*list(map(set, group)))
	for char in common:
		total += priority(char)

print(total)
