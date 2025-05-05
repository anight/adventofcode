#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split('[')
			checksum = t[1][:-1]
			t = t[0].rsplit('-', 1)
			sector_id = int(t[1])
			name = t[0]
			yield name, sector_id, checksum

# Part One

from collections import Counter

def gen_checksum(s):
	c = Counter(s.replace('-', ''))
	ordered = sorted( [(k, v) for k, v in c.items()],
		key=lambda item: (-item[1], item[0]) )
	return ''.join(k for k, _ in ordered[:5])


result = sum( sector_id for name, sector_id, checksum in load_data('input.txt') if gen_checksum(name) == checksum )

print(result)

# Part Two

from string import ascii_lowercase

def decipher(s, n):
	return ''.join( '-' if c == '-' else ascii_lowercase[(ord(c) - ord('a') + n) % 26] for c in s )

for name, sector_id, checksum in load_data('input.txt'):
	if decipher(name, sector_id).startswith('northpole'):
		break

print(sector_id)

