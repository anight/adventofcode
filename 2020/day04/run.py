#! /usr/bin/env python3

import re

def load_passports(filename):
	with open(filename, 'r') as f:
		p = {}
		for line in f:
			line = line.strip()
			if line == '':
				if len(p):
					yield p
					p = {}
				continue
			for t in line.split():
				key, value = t.split(':')
				p[key] = value
		if len(p):
			yield p

# Part One

total_valid = 0
for p in load_passports('input.txt'):
	def valid(p):
		required_keys = ( 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' )
		for key in required_keys:
			if key not in p:
				return False
		return True

	total_valid += valid(p)

print(total_valid)

# Part Two

total_valid = 0
for p in load_passports('input.txt'):
	def valid(p):
		constraints = {
			'byr': (r'^(\d{4})$', lambda g: 1920 <= int(g[0]) <= 2002),
			'iyr': (r'^(\d{4})$', lambda g: 2010 <= int(g[0]) <= 2020),
			'eyr': (r'^(\d{4})$', lambda g: 2020 <= int(g[0]) <= 2030),
			'hgt': (r'^(\d+)(in|cm)$', lambda g: {'in': 59, 'cm': 150}[g[1]] <= int(g[0]) <= {'in': 76, 'cm': 193}[g[1]]),
			'hcl': (r'^#[\da-f]{6}$', None),
			'ecl': (r'^(amb|blu|brn|gry|grn|hzl|oth)$', None),
			'pid': (r'^\d{9}$', None),
		}

		for field, (r, checker) in constraints.items():
			if field not in p:
				return False
			m = re.match(r, p[field])
			if not m:
				return False
			if checker is not None:
				if not checker(m.groups()):
					return False
		return True

	total_valid += valid(p)

print(total_valid)


