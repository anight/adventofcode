#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield re.split(r'\[|\]', line)

import re

# Part One

def has_abba(s):
	for i in range(len(s)-3):
		if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
			return True
	return False

result = 0

for ip in load_data('input.txt'):
	has = set()
	for i, s in enumerate(ip):
		type = i % 2
		if has_abba(s):
			has.add(type)
	if has == set([0]):
		result += 1

print(result)

# Part Two

def trios(s):
	aba = set()
	bab = set()
	for i in range(len(s)-2):
		if s[i] == s[i+2] and s[i] != s[i+1]:
			aba.add( (s[i], s[i+1]) )
			bab.add( (s[i+1], s[i]) )
	return aba, bab

result = 0

for ip in load_data('input.txt'):
	ips = set()
	hypernets = set()
	for i, s in enumerate(ip):
		type = i % 2
		aba, bab = trios(s)
		if type:
			hypernets |= bab
		else:
			ips |= aba
	if ips.intersection(hypernets):
		result += 1

print(result)
