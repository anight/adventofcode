#! /usr/bin/env python3

import re

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line

main = re.compile(r'^([\w\s]+) bags contain (.*)\.$')
contained = re.compile(r'(\d+) ([^,]+) bags?')

bags = {}

for line in load_data('input.txt'):
	m = main.fullmatch(line)
	parent = m.groups()[0]
	children = contained.findall(m.groups()[1])
	bags[parent] = children

# Part One

def contains(name, search):
	for _, child_name in bags[search]:
		if child_name == name:
			return True
		if contains(name, child_name):
			return True
	return False

total = sum( 1 for name in bags.keys() if contains('shiny gold', name) )

print(total)

# Part Two

def number_of_bags(name):
	return sum( int(num) * (1 + number_of_bags(child_name)) for num, child_name in bags[name] )

print(number_of_bags('shiny gold'))
