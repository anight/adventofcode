#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

import re
lines = list(load_data('input.txt'))

# Part One

result = 0

for line in lines:
	for m in re.findall(r'mul\(\d+,\d+\)', line):
		t = m[4:-1].split(',')
		result += int(t[0]) * int(t[1])

print(result)

# Part Two

result = 0

enabled = True

for line in lines:
	for m in re.findall(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', line):
		if m == 'do()':
			enabled = True
		elif m == 'don\'t()':
			enabled = False
		elif enabled:
			t = m[4:-1].split(',')
			result += int(t[0]) * int(t[1])

print(result)
