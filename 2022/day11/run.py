#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		lines = []
		for line in f:
			line = line.rstrip()
			if line == '':
				yield Monkey.from_text(lines)
				lines = []
			else:
				lines.append(line)
		yield Monkey.from_text(lines)

from typing import List, Callable
from functools import partial
from dataclasses import dataclass

@dataclass
class Monkey:

	num: int
	items: List[int]
	new_value: Callable[[int], int]
	test_div: int
	test_true: int
	test_false: int
	inspected: int = 0

	@staticmethod
	def from_text(lines):
		for line in lines:
			if line.startswith('Monkey '):
				num = int(line.split(' ')[1][:-1])
			elif line.startswith('  Starting items: '):
				items = list(map(int, line.split(': ')[1].split(', ')))
			elif line.startswith('  Operation: new = '):
				op1, op, op2 = line.split(' = ')[1].split(' ')
				def new_value(op1, op, op2, old_value):
					arg1 = int(op1) if op1.isnumeric() else old_value
					arg2 = int(op2) if op2.isnumeric() else old_value
					if op == "+":
						return arg1 + arg2
					return arg1 * arg2
			elif line.startswith('  Test: divisible by '):
				test_div = int(line.split(' by ')[1])
			elif line.startswith('    If true: throw to monkey '):
				test_true = int(line.split(' to monkey ')[1])
			elif line.startswith('    If false: throw to monkey '):
				test_false = int(line.split(' to monkey ')[1])
		return Monkey(num, items, partial(new_value, op1, op, op2), test_div, test_true, test_false)

	def turn(self, monkeys, divisor):
		while self.items:
			item = self.items.pop(0)
			new_value = self.new_value(item) // divisor
			if new_value % self.test_div == 0:
				throw_to = self.test_true
			else:
				throw_to = self.test_false
			monkeys[throw_to].items.append(new_value)
			self.inspected += 1

# Part One

monkeys = list(load_data('input.txt'))
for _ in range(20):
	for monkey in monkeys:
		monkey.turn(monkeys, 3)

most_active = sorted([m.inspected for m in monkeys], reverse=True)

print(most_active[0] * most_active[1])

# Part Two

class HugeUnknownNumber:
	def __init__(self, period, offset):
		self.period = period
		self.offset = offset

	def __mul__(self, x):
		match x:
			case int():
				return HugeUnknownNumber(self.period, (self.offset * x) % self.period)
			case HugeUnknownNumber():
				assert x.period == self.period
				return HugeUnknownNumber(self.period, (self.offset * x.offset) % self.period)

	def __floordiv__(self, x):
		assert type(x) is int
		assert x == 1
		return self

	def __mod__(self, x):
		assert type(x) is int
		assert self.period % x == 0
		return self.offset % x

	def __add__(self, x):
		assert type(x) is int
		return HugeUnknownNumber(self.period, (self.offset + x) % self.period)

monkeys = list(load_data('input.txt'))

period = 1
for monkey in monkeys:
	period *= monkey.test_div

for monkey in monkeys:
	for i in range(len(monkey.items)):
		monkey.items[i] = HugeUnknownNumber(period, monkey.items[i])

for _ in range(10000):
	for monkey in monkeys:
		monkey.turn(monkeys, 1)

most_active = sorted([m.inspected for m in monkeys], reverse=True)

print(most_active[0] * most_active[1])
