#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		pair = []
		for line in f:
			line = line.rstrip()
			if line == '':
				yield tuple(pair)
				pair = []
				continue
			pair.append(Packet(line))
		yield tuple(pair)

from copy import deepcopy
from functools import cmp_to_key

# Part One

class Packet:
	def __init__(self, expression):
		# Yes I could use eval(). No I won't use it
		current = list()
		stack = list()
		num = None
		for ch in expression:
			if ch == '[':
				assert num is None
				stack.append(current)
				current.append(list())
				current = current[-1]
			elif ch == ']':
				if num is not None:
					current.append(num)
					num = None
				current = stack.pop()
			elif ch == ',':
				if num is not None:
					current.append(num)
					num = None
			elif ch in '0123456789':
				digit = ord(ch) - ord('0')
				if num is None:
					num = digit
				else:
					num = 10 * num + digit
		self.packet = current[0]

	def __lt__(self, right):
		def cmp_lists(a, b):
			for i in range(min(len(a), len(b))):
				# Rule 3
				if type(a[i]) != type(b[i]):
					if type(a[i]) is int:
						a[i] = [a[i]]
					else:
						b[i] = [b[i]]
				# Rule 1
				if type(a[i]) is int and type(b[i]) is int:
					if a[i] != b[i]:
						return a[i] - b[i] < 0
				# Rule 2
				elif type(a[i]) is list and type(b[i]) is list:
					res = cmp_lists(a[i], b[i])
					if res is not None:
						return res
			if len(a) == len(b):
				return None
			return len(a) < len(b)
		return cmp_lists(deepcopy(self.packet), deepcopy(right.packet))

	def __repr__(self):
		return str(self.packet)

# Part One

total = 0
for i, (a, b) in enumerate(load_data('input.txt'), 1):
	if a < b:
		total += i

print(total)

# Part Two

divider1 = Packet('[[2]]')
divider2 = Packet('[[6]]')
all_packets = [ divider1, divider2 ]
for a, b in load_data('input.txt'):
	all_packets.append(a)
	all_packets.append(b)

s = sorted(all_packets, key=cmp_to_key(lambda a, b: -1 if a < b else 1))

print((s.index(divider1)+1) * (s.index(divider2)+1))
