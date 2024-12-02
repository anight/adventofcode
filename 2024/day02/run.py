#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split()))

data = list(load_data('input.txt'))

# Part One

def good(d):
	return (d == sorted(d) or d == sorted(d, reverse=True)) and \
		all( 1 <= abs(a - b) <= 3 for a, b in zip(d, d[1:]) )

result = sum( 1 for d in data if good(d) )

print(result)

# Part Two

result = 0

for d in data:
	if good(d):
		result += 1
	else:
		for i in range(len(d)):
			new_d = list(d)
			new_d.pop(i)
			if good(new_d):
				result += 1
				break

print(result)
