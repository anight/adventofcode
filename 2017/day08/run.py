#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield Instruction(line)

class Instruction:
	def __init__(self, s):
		t = s.split()
		self.reg = t[0]
		self.op = {'inc': add, 'dec': sub}[t[1]]
		self.value = int(t[2])
		self.cond_reg = t[4]
		self.cond_op = {'>': gt, '<': lt, '>=': ge, '<=': le, '==': eq, '!=': ne}[t[5]]
		self.cond_value = int(t[6])

	def __call__(self, state):
		if self.cond_op(state.get(self.cond_reg, 0), self.cond_value):
			state[self.reg] = self.op(state.get(self.reg, 0), self.value)

# Part One

from operator import add, sub, gt, lt, ge, le, eq, ne

state = dict()

for ins in load_data('input.txt'):
	ins(state)

print(max(state.values()))

# Part Two

state = dict()
result = 0

for ins in load_data('input.txt'):
	ins(state)
	result = max(result, *state.values())

print(result)
