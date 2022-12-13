#! /usr/bin/env python3

def all_samples(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.rstrip()

import re
from collections import namedtuple
from functools import cached_property
from operator import add, mul

class Lexer:
	whitespace_matcher = re.compile(r'\s*')
	number_matcher = re.compile(r'[0-9]+')

	class Token(namedtuple('Token', [])):
		pass
	class Value(namedtuple('Value', 'value')):
		pass
	class Number(Value):
		pass
	class ParenthesisOpen(Token):
		pass
	class ParenthesisClose(Token):
		pass
	class Asterisk(Token):
		pass
	class PlusSign(Token):
		pass
	class SyntaxError(Exception):
		pass

	def skip_leading_whitespace(self, s, pos) -> int:
		return self.whitespace_matcher.match(s, pos).end()

	def parse_number(self, s, pos):
		end = self.number_matcher.match(s, pos).end()
		assert end > pos
		return int(s[pos:end]), end

	def scan(self, s):
		pos = 0
		while True:
			pos = self.skip_leading_whitespace(s, pos)
			if pos == len(s):
				return
			char = s[pos]
			match char:
				case '(':
					yield Lexer.ParenthesisOpen()
					pos += 1
				case ')':
					yield Lexer.ParenthesisClose()
					pos += 1
				case char if char in '0123456789':
					num, pos = self.parse_number(s, pos)
					yield Lexer.Number(num)
				case '*':
					yield Lexer.Asterisk()
					pos += 1
				case '+':
					yield Lexer.PlusSign()
					pos += 1
				case _:
					raise Lexer.SyntaxError(f"Syntax error at position {pos}")

class Parser:

	class UnexpectedClosingParenthesis(Exception):
		pass

	class MissingClosingParenthesis(Exception):
		pass

	class UnexpectedOperator(Exception):
		pass

	class UnexpectedValue(Exception):
		pass

	def __init__(self, lexer):
		self.lexems = list(lexer)
		self.items = []
		self.parse()

	def closing_parenthesis(self, pos):
		nested = 0
		while pos < len(self.lexems):
			l = self.lexems[pos]
			match l:
				case Lexer.ParenthesisOpen():
					nested += 1
				case Lexer.ParenthesisClose():
					if nested == 0:
						return pos
					nested -= 1
			pos += 1
		raise Parser.MissingClosingParenthesis()

	def parse(self):
		pos = 0
		expect = 'value'
		while pos < len(self.lexems):
			l = self.lexems[pos]
			match l:
				case Lexer.ParenthesisOpen():
					if expect != 'value':
						raise Parser.UnexpectedValue()
					end = self.closing_parenthesis(pos+1)
					subexpression = self.__class__(self.lexems[pos+1:end])
					self.items.append(subexpression)
					pos = end + 1
					expect = 'op'
				case Lexer.ParenthesisClose():
					raise Parser.UnexpectedClosingParenthesis()
				case Lexer.Number() as num:
					if expect != 'value':
						raise Parser.UnexpectedValue()
					self.items.append(num)
					pos += 1
					expect = 'op'
				case Lexer.Asterisk():
					if expect != 'op':
						raise Parser.UnexpectedOperator()
					self.items.append(mul)
					pos += 1
					expect = 'value'
				case Lexer.PlusSign():
					if expect != 'op':
						raise Parser.UnexpectedOperator()
					self.items.append(add)
					pos += 1
					expect = 'value'

	def __repr__(self):
		return str(self.items)

# Part One

class ParserPartOne(Parser):

	@cached_property
	def value(self):
		acc = self.items[0].value
		for i in range(1, len(self.items), 2):
			op = self.items[i]
			arg = self.items[i+1]
			acc = op(acc, arg.value)
		return acc

result = 0
for line in all_samples('input.txt'):
	result += ParserPartOne(Lexer().scan(line)).value

print(result)

# Part Two

class ParserPartTwo(Parser):

	@cached_property
	def value(self):
		# first do all additions
		items = list(self.items)
		while add in items:
			i = items.index(add)
			result = add(items[i-1].value, items[i+1].value)
			items[i-1] = Lexer.Number(result)
			items.pop(i)
			items.pop(i)

		# do the rest
		acc = items[0].value
		for i in range(1, len(items), 2):
			op = items[i]
			arg = items[i+1]
			acc = op(acc, arg.value)
		return acc

result = 0
for line in all_samples('input.txt'):
	result += ParserPartTwo(Lexer().scan(line)).value

print(result)
