#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

from collections import Counter, defaultdict
from string import ascii_lowercase

def is_nice(string):
	c = Counter(string)
	vowels = sum( c[ch] for ch in 'aeiou' )
	has_doubles = any( ch+ch in string for ch in ascii_lowercase )
	has_illegal_pairs = any( pair in string for pair in ('ab', 'cd', 'pq', 'xy') )
	return vowels >= 3 and has_doubles and not has_illegal_pairs

result = sum(map(is_nice, load_data('input.txt')))

print(result)

# Part Two

def has_non_overlapping_pairs(string):
	c = defaultdict(int)
	last_pair = None
	for pair in zip(string, string[1:]):
		if last_pair == pair:
			last_pair = None
			continue
		c[pair] += 1
		last_pair = pair
	return any( v > 1 for v in c.values() )

def has_triplet(string):
	return any( trio[0] == trio[2] for trio in zip(string, string[1:], string[2:]) )

def is_nice(string):
	return has_non_overlapping_pairs(string) and has_triplet(string)

result = sum(map(is_nice, load_data('input.txt')))

print(result)
