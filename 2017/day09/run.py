#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		return f.readline().rstrip('\n')

# Part One

text = load_data('input.txt')

class Parser:
	def __init__(self):
		self.score = 0
		self.cancel = False
		self.garbage = False
		self.group_level = 0
		self.cleaned = 0

	def add_char(self, ch):
		if not self.garbage:
			if ch == '{':
				self.group_level += 1
			elif ch == '}':
				self.score += self.group_level
				self.group_level -= 1
			elif ch == '<':
				self.garbage = True
			return
		if self.cancel:
			self.cancel = False
			return
		if ch == '!':
			self.cancel = True
			return
		if ch == '>':
			self.garbage = False
			return
		self.cleaned += 1

p = Parser()

for ch in text:
	p.add_char(ch)

print(p.score)

# Part Two

print(p.cleaned)
