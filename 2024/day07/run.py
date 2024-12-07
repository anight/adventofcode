#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(': ')
			yield int(t[0]), list(map(int, t[1].split(' ')))

data = list(load_data('input.txt'))

# Part One

from itertools import product
from operator import mul, add

def total(*oplist):
	result = 0

	for r, args in data:
		for ops in product(oplist, repeat=len(args)-1):
			acc = args[0]
			for arg, op in zip(args[1:], ops):
				acc = op(acc, arg)
			if acc == r:
				break
		else:
			continue
		result += r

	return result

print(total(mul, add))

# Part Two

concat = lambda a, b: int(str(a) + str(b))

print(total(mul, add, concat))

