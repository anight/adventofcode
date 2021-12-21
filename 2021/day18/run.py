#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line

# Part One

class Pair(object):
	def __init__(self, s=None, arg1=None, arg2=None):
		if s is not None:
			self.value = self.parse(s)
		else:
			self.value = [arg1, arg2]

	def parse(self, s):
		assert s[0] == '[' and s[-1] == ']'
		scanned = []
		nested = 0
		value = None
		subvalue = ''
		for c in s[1:-1]:
			if c == '[':
				assert value is None
				nested += 1
				subvalue += c
			elif c == ']':
				assert value is None
				nested -= 1
				assert nested >= 0
				subvalue += c
				if nested == 0:
					value = Pair(s=subvalue)
					subvalue = ''
			elif c == ',':
				if nested == 0:
					scanned.append(value)
					value = None
				else:
					subvalue += c
			elif c in '0123456789':
				if nested == 0:
					if value is None:
						value = int(c)
					else:
						value *= 10
						value += int(c)
				else:
					subvalue += c
		if value is not None:
			scanned.append(value)
			value = None
		assert len(scanned) == 2
		return scanned

	def iterate_pairs_and_numbers(self, parent=None, i=None, nested=0):
		yield self, (parent, i), nested
		yield self.value[0], (self, 0), nested
		if type(self.value[0]) is Pair:
			yield from self.value[0].iterate_pairs_and_numbers(parent=self, i=0, nested=nested+1)
		yield self.value[1], (self, 1), nested
		if type(self.value[1]) is Pair:
			yield from self.value[1].iterate_pairs_and_numbers(parent=self, i=1, nested=nested+1)

	def find_first_explode(self):
		last_number = None
		explode = None
		first_number = None
		for value, (pair, i), nested in self.iterate_pairs_and_numbers():
			if explode is None:
				if type(value) is int:
					last_number = (pair, i)
				else:
					if nested == 4:
						assert type(value.value[0]) is int and type(value.value[1]) is int
						explode = (pair, i)
			else:
				if type(value) is int:
					if first_number is None and explode[0].value[explode[1]] is not pair:
						first_number = (pair, i)
		return last_number, explode, first_number

	def find_first_split(self):
		for value, (pair, i), _ in self.iterate_pairs_and_numbers():
			if type(value) is int and value >= 10:
				return pair, i
		return None

	def reduce(self):
		while True:
			last_number, explode, first_number = self.find_first_explode()
			if explode is not None:
				if last_number is not None:
					last_number[0].value[last_number[1]] += explode[0].value[explode[1]].value[0]
				if first_number is not None:
					first_number[0].value[first_number[1]] += explode[0].value[explode[1]].value[1]
				explode[0].value[explode[1]] = 0
				continue
			split = self.find_first_split()
			if split is not None:
				number = split[0].value[split[1]]
				split[0].value[split[1]] = Pair(arg1=number//2, arg2=number-number//2)
				continue
			break

	def add(self, pair):
		value = Pair(arg1=self.copy(), arg2=pair.copy())
		value.reduce()
		return value

	def copy(self):
		if type(self.value[0]) is int:
			arg1 = self.value[0]
		else:
			arg1 = self.value[0].copy()

		if type(self.value[1]) is int:
			arg2 = self.value[1]
		else:
			arg2 = self.value[1].copy()

		return Pair(arg1=arg1, arg2=arg2)


	def magnitude(self):
		if type(self.value[0]) is int:
			arg1 = self.value[0]
		else:
			arg1 = self.value[0].magnitude()

		if type(self.value[1]) is int:
			arg2 = self.value[1]
		else:
			arg2 = self.value[1].magnitude()

		return 3 * arg1 + 2 * arg2

	def __repr__(self):
		return 'Pair({},{})'.format(*self.value)

result = None

for line in load_data('input.txt'):
	p = Pair(s=line)
	if result is None:
		result = p
	else:
		result = result.add(p)

print(result.magnitude())

# Part Two

from itertools import combinations

pairs = [ Pair(s=line) for line in load_data('input.txt') ]

largest = None

for a, b in combinations(pairs, 2):
	magnitude = a.add(b).magnitude()
	if largest is None:
		largest = magnitude
	else:
		if largest < magnitude:
			largest = magnitude
	magnitude = b.add(a).magnitude()
	if largest is None:
		largest = magnitude
	else:
		if largest < magnitude:
			largest = magnitude

print(largest)

