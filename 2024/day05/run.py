#! /usr/bin/env python3

def load_data(filename):
	orders = []
	updates = []
	parse_orders = True
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				parse_orders = False
			elif parse_orders:
				orders.append(tuple(map(int, line.split('|'))))
			else:
				updates.append(list(map(int, line.split(','))))
	return set(orders), updates

orders, updates = load_data('input.txt')

# Part One

def in_order(u):
	for a, b in orders:
		if a in u and b in u[:u.index(a)]:
			return False
	return True

result = sum( u[len(u)//2] for u in updates if in_order(u) )

print(result)

# Part Two

from itertools import combinations

def fix_order(u):
	while True:
		for a, b in combinations(u, 2):
			a_i = u.index(a)
			b_i = u.index(b)
			if (a, b) in orders and a_i > b_i:
				break
			if (b, a) in orders and b_i > a_i:
				break
		else:
			return
		u[a_i], u[b_i] = u[b_i], u[a_i]

result = 0

for u in updates:
	if in_order(u):
		continue
	fix_order(u)
	result += u[len(u)//2]

print(result)
