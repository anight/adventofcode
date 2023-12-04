#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			c, lists = line.rstrip('\n').split(': ')
			c_id = int(c.split()[1])
			w_list, my_list = lists.split(' | ')
			yield c_id, set(w_list.split()), set(my_list.split())

# Part One

import math

def score(w_list, my_list):
	return int(math.floor(2 ** (len(w_list.intersection(my_list))-1)))

total = sum( score(w_list, my_list) for _, w_list, my_list in load_data('input.txt') )

print(total)


# Part Two

from collections import defaultdict

copies = defaultdict(lambda: 0)

total = 0

for c_id, w_list, my_list in load_data('input.txt'):
	s = len(w_list.intersection(my_list))
	for copy_c_id in range(c_id + 1, c_id + 1 + s):
		copies[copy_c_id] += 1 + copies[c_id]
	total += 1 + copies[c_id]

print(total)
