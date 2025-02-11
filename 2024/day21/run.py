#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

codes = list(load_data('input.txt'))

# Part One

from functools import cache
from collections import defaultdict, Counter

class Keypad:

	@classmethod
	@cache
	def xy(cls, key):
		for y in range(len(cls.keypad)):
			if key in cls.keypad[y]:
				return cls.keypad[y].index(key), y
		raise Exception(f"Key {key} not found in {cls}")

	@classmethod
	@cache
	def paths(cls, from_, to):
		def is_valid(x, y, path):
			for step in path:
				dx, dy = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}[step]
				x += dx
				y += dy
				if cls.keypad[y][x] is None:
					return False
			return True
		fx, fy = cls.xy(from_)
		tx, ty = cls.xy(to)
		dx = '<' * (fx-tx) if tx < fx else '>' * (tx-fx)
		dy = '^' * (fy-ty) if ty < fy else 'v' * (ty-fy)
		return set([dx+dy+'A'] * is_valid(fx, fy, dx+dy) + [dy+dx+'A'] * is_valid(fx, fy, dy+dx))

	@classmethod
	@cache
	def shortest_from_to(cls, from_, to, backed):
		paths = cls.paths(from_, to)
		if not backed:
			return next(iter(paths))
		min_path = min( [DirKeypad.shortest_seq(path, backed-1) for path in paths], key=len )
		return min_path

	@classmethod
	@cache
	def shortest_seq(cls, code, backed):
		ret = ''
		current = 'A'
		for c in code:
			ret += cls.shortest_from_to(current, c, backed)
			current = c
		return ret








	@classmethod
	@cache
	def shortest_path(cls, from_, to):
		paths = cls.paths(from_, to)
		min_path = min( [(DirKeypad.shortest_seq(path, 5), path) for path in paths], key=lambda item: len(item[0]) )[1]
		return min_path

	@staticmethod
	def str2tokens(s):
		assert s[-1] == 'A'
		return [ t + 'A' for t in s.split('A')[:-1] ]

	@classmethod
	def str2cnt(cls, s):
		return Counter(cls.str2tokens(s))

	@staticmethod
	def length(code):
		return sum([ len(k) * v for k, v in code.items() ])

	@classmethod
	@cache
	def move(cls, key):
		current = 'A'
		ret = []
		for c in key:
			ret.append(cls.shortest_path(current, c))
			current = c
		return ret

	@classmethod
	def shortest_path_quick(cls, code, backed):
		if not backed:
			return cls.length(code)
		ret = defaultdict(int)
		for k, v in code.items():
			for m in DirKeypad.move(k):
				ret[m] += v
		return DirKeypad.shortest_path_quick(ret, backed-1)

	@classmethod
	def shortest_seq_quick(cls, code, backed):
		code = ''.join(cls.move(code))
		code = cls.str2cnt(code)
		return cls.shortest_path_quick(code, backed)

class NumKeypad(Keypad):
	keypad = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', 'A']]

class DirKeypad(Keypad):
	keypad = [[None, '^', 'A'], ['<', 'v', '>']]

def length(code, robots):
	return len(NumKeypad.shortest_seq(code, robots))

def score(code, robots):
	return length(code, robots) * int(code[:-1])

result = sum( score(code, 2) for code in codes )

print(result)

# Part Two

def score2(code, robots):
	return NumKeypad.shortest_seq_quick(code, robots) * int(code[:-1])

result = sum( score2(code, 25) for code in codes )

print(result)
