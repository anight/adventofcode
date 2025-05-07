#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield Input.parse(line) or GivesLowHigh.parse(line)

class Base:
	@classmethod
	def parse(cls, s):
		match = re.match(cls.pattern, s)
		if match:
			return cls(match)
		else:
			return None

	def __repr__(self):
		return f'{self.__class__.__name__}'

class Input(Base):
	pattern = r'^value (?P<value>\d+) goes to bot (?P<bot>\d+)$'

	def __init__(self, match):
		self.bot = int(match.group('bot'))
		self.value = int(match.group('value'))

class GivesLowHigh(Base):
	pattern = r'^bot (?P<bot>\d+) gives low to (?P<low_type>bot|output) (?P<low_id>\d+) and high to (?P<high_type>bot|output) (?P<high_id>\d+)$'

	def __init__(self, match):
		self.bot = int(match.group('bot'))
		self.low_type = match.group('low_type')
		self.low_id = int(match.group('low_id'))
		self.high_type = match.group('high_type')
		self.high_id = int(match.group('high_id'))

class State:
	def __init__(self):
		self.bots = {}
		self.bots_with_two_values = set()
		self.instructions = {}
		self.outputs = {}

	def add_bot_value(self, bot, value):
		if bot not in self.bots:
			self.bots[bot] = [value]
		else:
			assert len(self.bots[bot]) == 1
			if value < self.bots[bot][0]:
				self.bots[bot].insert(0, value)
			else:
				self.bots[bot].append(value)
			self.bots_with_two_values.add(bot)

	def add_value(self, type, id, value):
		if type == 'bot':
			self.add_bot_value(id, value)
		else:
			self.outputs[id] = value

	def remove_bot_values(self, bot):
		del self.bots[bot]
		self.bots_with_two_values.remove(bot)

	def add_ins(self, ins):
		if type(ins) is Input:
			self.add_bot_value(ins.bot, ins.value)
		elif type(ins) is GivesLowHigh:
			self.instructions[ins.bot] = ins

	def run(self, hook):
		while self.bots_with_two_values:
			bot = next(iter(self.bots_with_two_values))
			ins = self.instructions[bot]
			value_low, value_high = self.bots[bot]
			hook(ins.bot, value_low, value_high)
			self.remove_bot_values(bot)
			self.add_value(ins.low_type, ins.low_id, value_low)
			self.add_value(ins.high_type, ins.high_id, value_high)

# Part One

import re

s = State()

for ins in load_data('input.txt'):
	s.add_ins(ins)

def hook(bot, value_low, value_high):
	if value_low == 17 and value_high == 61:
		print(bot)

s.run(hook)

# Part Two

print(s.outputs[0] * s.outputs[1] * s.outputs[2])

