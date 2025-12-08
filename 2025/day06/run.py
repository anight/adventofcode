#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		nums = []
		ops = []
		for line in f:
			line = line.rstrip('\n')
			if line.startswith('+') or line.startswith('*'):
				ops = list(map(lambda x: add if x == '+' else mul, line.split()))
			else:
				nums.append(list(map(int, line.split())))
		return nums, ops

from operator import add, mul
from functools import reduce

nums, ops = load_data('input.txt')

# Part One

print(sum(reduce(op, col) for op, col in zip(ops, zip(*nums))))

# Part Two

with open('input.txt') as f:
	num_lines = f.read().split('\n')[:-2]

def group_columns():
	group = []
	for col in zip(*num_lines):
		n = ''.join(col).strip()
		if n == '':
			yield group
			group = []
			continue
		group.append(int(n))
	yield group

print(sum(
	reduce(op, group, 0 if op is add else 1)
	for op, group in zip(ops, group_columns())
))
