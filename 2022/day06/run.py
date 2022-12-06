#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

def find_sequence(cnt, line):
	for i in range(len(line)-cnt):
		if cnt == len(set(line[i:i+cnt])):
			return cnt + i

# Part One

result = find_sequence(4, next(load_data('input.txt')))
print(result)

# Part Two

result = find_sequence(14, next(load_data('input.txt')))
print(result)
