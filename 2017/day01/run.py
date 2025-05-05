#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return list(map(int, line))

digits = load_data('input.txt')

# Part One

result = sum( a * (a == b) for a, b in zip(digits, digits[1:] + digits[:1]) )

print(result)

# Part Two

m = len(digits)//2

result = sum( a * (a == b) for a, b in zip(digits, digits[m:] + digits[:m]) )

print(result)
