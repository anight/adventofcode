#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		p = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				yield p[0], p[1], p[2]
				p = []
			else:
				t = line.split(': ')[1].split(', ')
				p.append( (int(t[0][2:]), int(t[1][2:])) )
		yield p[0], p[1], p[2]

data = list(load_data('input.txt'))

# Part One

result = 0

for a, b, prize in data:
	for n_b in range(100, -1, -1):
		n_a = min( (prize[0] - b[0] * n_b) // a[0], (prize[1] - b[1] * n_b) // a[1] )
		if n_a < 0 or n_a > 100:
			continue
		if n_a * a[0] + n_b * b[0] == prize[0] and n_a * a[1] + n_b * b[1] == prize[1]:
			result += n_a * 3 + n_b * 1
			break

print(result)

# Part Two

from sympy.solvers.diophantine import diop_solve
from sympy import symbols, solve, Eq
n_a, n_b, t1, t2 = symbols('n_a n_b t1 t2', integer=True)

result = 0

add = int(1e13)

for a, b, prize in data:
	e1 = a[0] * n_a + b[0] * n_b - prize[0] - add
	e2 = a[1] * n_a + b[1] * n_b - prize[1] - add
	s1 = diop_solve(e1, param=t1)
	s2 = diop_solve(e2, param=t2)
	if s1 == (None, None) or s2 == (None, None):
		# No solution, for example, an odd number cannot be represented as sum of even numbers
		continue
	e = [Eq(n_a, s1[0]), Eq(n_b, s1[1]), Eq(n_a, s2[0]), Eq(n_b, s2[1])]
	s = solve(e, dict=True)
	if len(s) == 0:
		# No solution, for example two lines are parallel
		continue
	n_a_value, n_b_value = s[0][n_a], s[0][n_b]
	if n_a_value < 0 or n_b_value < 0:
		# Not a solution by problem statement
		continue
	result += n_a_value * 3 + n_b_value * 1

print(result)
