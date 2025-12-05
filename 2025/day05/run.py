#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		ranges = []
		ingredients = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				break
			t = line.split('-')
			ranges.append( (int(t[0]), int(t[1])) )
		for line in f:
			line = line.rstrip('\n')
			ingredients.append(int(line))
		return ranges, ingredients

ranges, ingredients = load_data('input.txt')

# Part One

is_fresh = lambda i: any( f <= i <= t for f, t in ranges )
print(sum(map(is_fresh, ingredients)))

# Part Two

import portion as P
from functools import reduce

all_ranges = reduce(lambda a, b: a | b, [P.closed(f, t) for f, t in ranges])
print(sum(i.upper - i.lower + 1 for i in all_ranges))
