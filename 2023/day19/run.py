#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		all_rules = {}
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				break
			name = line.split('{')[0]
			rules = line[len(name)+1:-1].split(',')
			all_rules[name] = list(map(Rule.from_string, rules))
		all_parts = []
		for line in f:
			line = line.rstrip('\n')
			part = {}
			for category in line[1:-1].split(','):
				name, value = category.split('=')
				part[name] = int(value)
			all_parts.append(part)
		return all_rules, all_parts

# Part One

from dataclasses import dataclass
from operator import gt, lt

@dataclass
class Rule:
	category: str
	compare: callable
	value: int
	target: str

	@classmethod
	def from_string(cls, s):
		if ':' in s:
			condition, target = s.split(':')
			category = condition[0]
			compare = {'<': lt, '>': gt}[condition[1]]
			value = int(condition[2:])
			return cls(category, compare, value, target)
		else:
			return cls('', None, 0, s)

	def apply(self, part):
		if self.compare is None:
			return self.target
		if self.compare(part[self.category], self.value):
			return self.target
		return None

def part_accepted(part, all_rules):
	rules_list = all_rules['in']
	while True:
		for rule in rules_list:
			target = rule.apply(part)
			if target == 'A':
				return True
			if target == 'R':
				return False
			if target is None:
				continue
			rules_list = all_rules[target]
			break

all_rules, all_parts = load_data('input.txt')

total = sum( sum(part.values()) for part in all_parts if part_accepted(part, all_rules) )

print(total)

# Part Two

from discrete_volume_storage import DiscreteVolumeStorage

dvs = DiscreteVolumeStorage()

class Tracer:
	def __init__(self, rule, limits):
		self.rule = rule
		self.limits = list(limits)

	@staticmethod
	def split_limits(compare, value, limits):
		f, t = limits
		if compare is gt:
			return f, value+1, value+1, t
		else:
			return value, t, f, value

	def branch(self, rule):
		limit_index = 'xmas'.index(rule.category)
		new_from, new_to, branched_from, branched_to = self.split_limits(rule.compare, rule.value, self.limits[limit_index])
		self.limits = self.limits[:limit_index] + [(new_from, new_to)] + self.limits[limit_index+1:]
		branched_limits = self.limits[:limit_index] + [(branched_from, branched_to)] + self.limits[limit_index+1:]
		return Tracer(rule.target, branched_limits)

to_trace = [ Tracer('in', [(1, 4001)] * 4) ]

while len(to_trace) > 0:
	tracer = to_trace.pop()
	if tracer.rule == 'A':
		dvs.set(tracer.limits, 1)
		continue
	if tracer.rule == 'R':
		dvs.set(tracer.limits, 0)
		continue
	for rule in all_rules[tracer.rule]:
		if rule.compare is None:
			to_trace.append(Tracer(rule.target, tracer.limits))
		else:
			to_trace.append(tracer.branch(rule))

print(dvs.volume())
