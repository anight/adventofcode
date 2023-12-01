#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.rstrip('\n')

# Part One

def calibration_value(line):
	digits = ''.join(filter(lambda ch: ch.isdigit(), line))
	return int(digits[0] + digits[-1])

print(sum( calibration_value(line) for line in load_data('input.txt') ))

# Part Two

import re

digits_as_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

first_re = re.compile(r'(\d|' + '|'.join(digits_as_words) + ')')
last_re = re.compile(r'(\d|' + '|'.join([ w[::-1] for w in digits_as_words ]) + ')')

def calibration_value(line):
	m = first_re.search(line).group(0)
	first_digit = m if m.isdigit() else str(1+digits_as_words.index(m))
	m = last_re.search(line[::-1]).group(0)
	last_digit = m if m.isdigit() else str(1+digits_as_words.index(m[::-1]))
	return int(first_digit + last_digit)

print(sum( calibration_value(line) for line in load_data('input.txt') ))
