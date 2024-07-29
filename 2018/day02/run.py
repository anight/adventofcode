#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

from collections import Counter

twice = 0
three = 0

for box_id in load_data('input.txt'):
	cnt = Counter(box_id).values()
	twice += (2 in cnt)
	three += (3 in cnt)

print(twice * three)

# Part Two

from itertools import combinations

for box_id1, box_id2 in combinations(load_data('input.txt'), 2):
	if sum(box_id1[i] != box_id2[i] for i in range(len(box_id1))) == 1:
		break
else:
	raise("oops")

common_letters = [ box_id1[i] for i in range(len(box_id1)) if box_id1[i] == box_id2[i] ]

print(''.join(common_letters))

