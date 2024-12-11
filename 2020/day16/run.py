#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		rules = []
		my_ticket = None
		nearby_tickets = []
		for line in f:
			line = line.strip()
			if line == '':
				break
			name, ranges = line.split(': ')
			ranges = ranges.split(' or ')
			s = set()
			for r in ranges:
				numbers = r.split('-')
				s |= set(range(int(numbers[0]), int(numbers[1])+1))
			rules.append( (name, s) )

		f.readline()
		my_ticket = list(map(int, f.readline().strip().split(',')))

		f.readline()
		f.readline()
		for line in f:
			ticket = list(map(int, line.strip().split(',')))
			nearby_tickets.append(ticket)

		return rules, my_ticket, nearby_tickets

import numpy as np

# Part One

rules, my_ticket, nearby_tickets = load_data('input.txt')

all_rules = set()
for _, valid_numbers in rules:
	all_rules |= valid_numbers

total_invalid = 0
for ticket in list(nearby_tickets):
	for n in ticket:
		if n not in all_rules:
			total_invalid += n
			nearby_tickets.remove(ticket)
			break

print(total_invalid)

# Part Two

field_map = {}
nearby_tickets = np.array(nearby_tickets)
for rule_no, (name, s) in enumerate(rules):
	possible_fields = set()
	for field_no in range(nearby_tickets.shape[1]):
		if all( x in s for x in nearby_tickets[:,field_no] ):
			possible_fields.add(field_no)
	field_map[rule_no] = possible_fields

found = []
while not all( 1 == len(s) for s in field_map.values() ):
	for v in field_map.values():
		if 1 == len(v) and v not in found:
			found.append(v)
			for vv in field_map.values():
				if v is vv:
					continue
				vv.difference_update(v)

total = 1
for rule_no, (name, _) in enumerate(rules):
	if name.startswith('departure'):
		field_no = list(field_map[rule_no])[0]
		total *= my_ticket[field_no]

print(total)
