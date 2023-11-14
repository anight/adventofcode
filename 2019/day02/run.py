#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip()
		return map(int, line.split(','))

# Part One

from operator import add, mul

class IntcodeComputer:

	def __init__(self, data):
		self.data = list(data)

	def run(self, noun, verb):
		self.data[1] = noun
		self.data[2] = verb
		ptr = 0
		while self.data[ptr] != 99:
			op, arg1, arg2, out = self.data[ptr:ptr+4]
			self.data[out] = {1: add, 2: mul}[op](self.data[arg1], self.data[arg2])
			ptr += 4
		return self.data[0]

c = IntcodeComputer(load_data('input.txt'))
result = c.run(12, 2)

print(result)

# Part Two

import itertools

for noun, verb in itertools.product(range(0, 100), repeat=2):
	c = IntcodeComputer(load_data('input.txt'))
	result = c.run(noun, verb)
	if result == 19690720:
		break
else:
	raise Exception("oops")

print(100 * noun + verb)
