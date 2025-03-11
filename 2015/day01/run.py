#! /usr/bin/env python3

# Part One

line = open('input.txt').readline()

from collections import Counter
from operator import sub

result = sub(*Counter(line).values())

print(result)

# Part Two

level = 0
for i, ch in enumerate(line):
	level += {'(': 1, ')': -1}[ch]
	if level == -1:
		break

print(1 + i)

