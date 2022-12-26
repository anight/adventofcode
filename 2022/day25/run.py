#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

def from_snafu(s):
	res = 0
	for ch in s:
		res = 5 * res + ("=-012".index(ch) - 2)
	return res

def to_snafu(n):
	digit = n % 5
	rest = n // 5 + (digit > 2)
	return (to_snafu(rest) if rest > 0 else '') + str("=-012"[(digit + 2) % 5])

# Part One

result = sum( from_snafu(s) for s in load_data('input.txt') )

print(to_snafu(result))
