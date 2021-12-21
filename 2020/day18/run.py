#! /usr/bin/env python3

from calculator import calculate, ParserPartOne, ParserPartTwo

def all_samples(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.strip()

result = 0
for line in all_samples('input.txt'):
	result += calculate(ParserPartOne, line)

print(result)

result = 0
for line in all_samples('input.txt'):
	result += calculate(ParserPartTwo, line)

print(result)
