#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			m = re.match(r'^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.$', line).groups()
			yield m[0], (-1 if m[1] == 'lose' else 1) * int(m[2]), m[3]

# Part One

import re
from itertools import permutations

preferences = {}
for who, score, withwhom in load_data('input.txt'):
	if who not in preferences:
		preferences[who] = {}
	preferences[who][withwhom] = score

attendees = set(preferences.keys())

def happiness(order):
	total = 0
	for i, who in enumerate(order):
		total += preferences[who].get(order[i-1], 0)
		total += preferences[who].get(order[(i+1) % len(order)], 0)
	return total

result = max( happiness(order) for order in permutations(attendees) )

print(result)

# Part Two

preferences["Me"] = {}
attendees.add("Me")

result = max( happiness(order) for order in permutations(attendees) )

print(result)
