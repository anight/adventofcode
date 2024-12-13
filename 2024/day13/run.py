#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		p = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				yield p
				p = []
			else:
				t = line.split(': ')[1].split(', ')
				p.append( np.array([int(t[0][2:]), int(t[1][2:])] ) )
		yield p

import numpy as np

data = list(load_data('input.txt'))

# Part One

def solve1(a, b, prize):
	x = np.linalg.solve([[a[0], b[0]], [a[1], b[1]]], prize)
	if np.all(np.isclose(x, np.round(x))) and np.all(0 <= x) and np.all(x <= 100):
		return np.dot(np.round(x).astype(int), [3, 1])
	return 0

result = sum( solve1(a, b, prize) for a, b, prize in data )

print(result)

# Part Two

from sympy import symbols, solve, Eq
n_a, n_b = symbols('n_a n_b', integer=True)

def solve2(a, b, prize):
	e1 = Eq(a[0] * n_a + b[0] * n_b, prize[0])
	e2 = Eq(a[1] * n_a + b[1] * n_b, prize[1])
	s = solve({e1, e2}, dict=True)
	if s:
		return s[0][n_a] * 3 + s[0][n_b]
	return 0

result = sum( solve2(a, b, prize+int(1e13)) for a, b, prize in data )

print(result)
