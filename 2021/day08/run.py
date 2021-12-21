#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			z, o = line.split(' | ')
			z = z.split()
			o = o.split()
			yield z, o

# Part One

num = 0

for zerotonine, output in load_data('input.txt'):
	for o in output:
		if len(o) in (2, 3, 4, 7):
			num += 1

print(num)

# Part Two

from itertools import permutations

def solve(zerotonine):
	digits = [
		'abcefg',   # 0
		'cf',       # 1
		'acdeg',    # 2
		'acdfg',    # 3
		'bcdf',     # 4
		'abdfg',    # 5
		'abdefg',   # 6
		'acf',      # 7
		'abcdefg',  # 8
		'abcdfg',   # 9
	]

	found = False

	for p in permutations('abcdefg'):
		encode_table = str.maketrans('abcdefg', ''.join(p))
		test_digits = [ set(d.translate(encode_table)) for d in digits ]
		for z in zerotonine:
			if set(z) not in test_digits:
				break
			test_digits.remove(set(z))
		if len(test_digits) == 0:
			found = True
			break

	assert found

	encoded_digits = [ set(d.translate(encode_table)) for d in digits ]
	def decoder(n):
		return encoded_digits.index(set(n))
	return decoder


num = 0

for zerotonine, output in load_data('input.txt'):
	decoder = solve(zerotonine)
	value = 0
	for o in output:
		value *= 10
		value += decoder(o)
	num += value

print(num)
