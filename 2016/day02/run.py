#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

def code(pad):
	code = ''
	pos = 0

	for line in load_data('input.txt'):
		for c in line:
			d = {'U': -1j, 'D': 1j, 'L': -1, 'R': 1}[c]
			if pos+d not in pad:
				continue
			pos += d
		code += pad[pos]

	return code

# Part One

pad = { -1-1j: '1', 0-1j: '2', 1-1j: '3',
        -1+0j: '4', 0+0j: '5', 1+0j: '6',
        -1+1j: '7', 0+1j: '8', 1+1j: '9' }

print(code(pad))

# Part Two

pad = { 0-2j: '1',
        -1-1j: '2', 0-1j: '3', 1-1j: '4',
        -2+0j: '5', -1+0j: '6', 0+0j: '7', 1+0j: '8', 2+0j: '9',
        -1+1j: 'A', 0+1j: 'B', 1+1j: 'C',
        0+2j: 'D' }

print(code(pad))
