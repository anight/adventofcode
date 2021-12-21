#! /usr/bin/env python3

from itertools import combinations

numbers = []

with open('input.txt', 'r') as f:
	for line in f:
		n = int(line)
		numbers.append(n)

for a, b in combinations(numbers, 2):
	if a + b == 2020:
		print(a * b)
		break

for a, b, c in combinations(numbers, 3):
	if a + b + c == 2020:
		print(a * b * c)
		break
