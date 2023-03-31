#! /usr/bin/env python3

def all_passwords():
	with open('input.txt', 'r') as f:
		for line in f:
			tokens = line.strip().split(' ')
			char = tokens[1].strip(':')
			from_to = tokens[0].split('-')
			yield int(from_to[0]), int(from_to[1]), char, tokens[2]

valid = 0
for n_from, n_to, char, passwd in all_passwords():
	n = passwd.count(char)
	if n_from <= n <= n_to:
		valid += 1

print(valid)

valid = 0
for n_from, n_to, char, passwd in all_passwords():
	if (passwd[n_from-1] == char) != (passwd[n_to-1] == char):
		valid += 1

print(valid)

