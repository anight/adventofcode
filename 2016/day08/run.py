#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield Rect.parse(line) or RotateRow.parse(line) or RotateColumn.parse(line)

class Base:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	@classmethod
	def parse(cls, s):
		match = re.match(cls.pattern, s)
		if match:
			return cls(int(match.group('a')), int(match.group('b')))
		else:
			return None

	def __repr__(self):
		return f'{self.__class__.__name__}(a={self.a}, b={self.b})'

class Rect(Base):
	pattern = r'rect (?P<a>\d+)x(?P<b>\d+)'

	def __call__(self, screen):
		screen[:self.b,:self.a] = 1

class RotateRow(Base):
	pattern = r'rotate row y=(?P<a>\d+) by (?P<b>\d+)'

	def __call__(self, screen):
		screen[self.a:self.a+1,:] = np.hstack((screen[self.a:self.a+1,-self.b:], screen[self.a:self.a+1,:-self.b]))

class RotateColumn(Base):
	pattern = r'rotate column x=(?P<a>\d+) by (?P<b>\d+)'

	def __call__(self, screen):
		screen[:,self.a:self.a+1] = np.vstack((screen[-self.b:,self.a:self.a+1], screen[:-self.b,self.a:self.a+1]))

# Part One

import re
import numpy as np

screen = np.zeros((6, 50), dtype=int)

for cmd in load_data('input.txt'):
	cmd(screen)

print(np.sum(screen))

# Part Two

for line in screen:
	print(''.join(map(str, line)).replace('1', '#').replace('0', '.'))

