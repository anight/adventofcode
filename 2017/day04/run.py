#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

def valid(password):
	words = password.split(' ')
	return len(words) == len(set(words))

result = sum( valid(password) for password in load_data('input.txt') )

print(result)

# Part Two

def valid(password):
	words = [ ''.join(sorted(word)) for word in password.split(' ') ]
	return len(words) == len(set(words))

result = sum( valid(password) for password in load_data('input.txt') )

print(result)
