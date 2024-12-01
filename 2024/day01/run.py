#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split()
			yield int(t[0]), int(t[1])

l1, l2 = zip(*list(load_data('input.txt')))

# Part One

result = sum( abs(a - b) for a, b in zip(sorted(l1), sorted(l2)) )

print(result)

# Part Two

result = sum( a * l2.count(a) for a in l1 )

print(result)

