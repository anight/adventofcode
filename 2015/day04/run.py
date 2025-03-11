#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

key = next(load_data('input.txt'))

# Part One

import hashlib

def find_zeros(z):
	n = 0
	while True:
		m = hashlib.md5()
		m.update(bytes(key, 'ascii'))
		m.update(bytes(str(n), 'ascii'))
		if m.hexdigest().startswith('0' * z):
			break
		n += 1
	return n

print(find_zeros(5))

# Part Two

print(find_zeros(6))

