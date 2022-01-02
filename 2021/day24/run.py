#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			t = line.split()
			if len(t) > 2 and (t[2].isnumeric() or t[2].startswith('-')):
				t[2] = int(t[2])
			yield tuple(t)

# Part One

class ALU:
	regs = ('x', 'y', 'z', 'w')

	def __init__(self):
		self.values = {}
		self.reset()
		self.code = []
		self.input = None

	def reset(self):
		self.values = dict(zip(self.regs, [0] * len(self.regs)))

	def load(self, code):
		self.code = code
		self.instruction_ptr = 0

	def run(self, input):
		self.input = input
		self.input_ptr = 0
		while self.instruction_ptr < len(self.code):
			self.execute_op(self.code[self.instruction_ptr])
			self.instruction_ptr += 1

	def execute_op(self, op):
		name, args = op[0], op[1:]
		method = getattr(self, 'op_{}'.format(name))
		method(*args)

	def op_inp(self, reg):
		assert reg in self.regs
		self.values[reg] = int(self.input[self.input_ptr])
		self.input_ptr += 1

	def op_add(self, reg, arg):
		assert reg in self.regs
		if type(arg) is int:
			self.values[reg] += arg
		else:
			assert arg in self.regs
			self.values[reg] += self.values[arg]

	def op_mul(self, reg, arg):
		assert reg in self.regs
		if type(arg) is int:
			self.values[reg] *= arg
		else:
			assert arg in self.regs
			self.values[reg] *= self.values[arg]

	def op_mod(self, reg, arg):
		assert reg in self.regs
		assert self.values[reg] >= 0
		if type(arg) is int:
			assert arg > 0
			self.values[reg] %= arg
		else:
			assert arg in self.regs
			assert self.values[arg] >= 0
			self.values[reg] %= self.values[arg]

	def op_div(self, reg, arg):
		assert reg in self.regs
		if type(arg) is int:
			assert arg != 0
			self.values[reg] = int(self.values[reg] / arg)
		else:
			assert arg in self.regs
			assert self.values[arg] != 0
			self.values[reg] = int(self.values[reg] / self.values[arg])

	def op_eql(self, reg, arg):
		assert reg in self.regs
		if type(arg) is int:
			self.values[reg] = int(self.values[reg] == arg)
		else:
			assert arg in self.regs
			self.values[reg] = int(self.values[reg] == self.values[arg])

code = list(load_data('input.txt'))

def f_alu(number):
	alu = ALU()
	alu.reset()
	alu.load(code)
	alu.run(number)
	return alu.values['z']

v1, v2, v3 = [], [], []

pattern = [
	('inp', 'w'),
	('mul', 'x', 0),
	('add', 'x', 'z'),
	('mod', 'x', 26),
	('div', 'z', v1),
	('add', 'x', v2),
	('eql', 'x', 'w'),
	('eql', 'x', 0),
	('mul', 'y', 0),
	('add', 'y', 25),
	('mul', 'y', 'x'),
	('add', 'y', 1),
	('mul', 'z', 'y'),
	('mul', 'y', 0),
	('add', 'y', 'w'),
	('add', 'y', v3),
	('mul', 'y', 'x'),
	('add', 'z', 'y'),
]

assert len(code) % len(pattern) == 0

for i in range(0, len(code), len(pattern)):
	for j in range(len(pattern)):
		assert len(code[i+j]) == len(pattern[j])
		for k in range(len(code[i+j])):
			if type(pattern[j][k]) is list:
				pattern[j][k].append(code[i+j][k])
			else:
				assert pattern[j][k] == code[i+j][k]

assert v1.count(1) == v1.count(26)
assert len(v1) == v1.count(1) + v1.count(26)

def f_reverse_engineered(number):
	def iteration(z, w, i):
		if w != ((z % 26) + v2[i]):
			z = int(z / v1[i]) * 26 + (w + v3[i])
		else:
			z = int(z / v1[i])
		return z
	z = 0
	for i, w in enumerate(str(number)):
		z = iteration(z, int(w), i)
	return z

def pairs():
	s = []
	for i, v in enumerate(v1):
		if v == 1:
			s.append(i)
			continue
		one = s.pop()
		twentysix = i
		yield one, twentysix

# get max number

number = [0] * 14

for one, twentysix in pairs():
	d = v2[twentysix] + v3[one]
	if d < 0:
		assert d > -9
		number[one] = 9
		number[twentysix] = 9 + d
	else:
		assert d < 9
		number[one] = 9 - d
		number[twentysix] = 9

number = ''.join(map(str, number))

assert 0 == f_alu(number)
assert 0 == f_reverse_engineered(number)

print(number)

# Part Two

# get min number

number = [0] * 14

for one, twentysix in pairs():
	d = v2[twentysix] + v3[one]
	if d > 0:
		assert d < 9
		number[one] = 1
		number[twentysix] = 1 + d
	else:
		assert d > -9
		number[one] = 1 - d
		number[twentysix] = 1

number = ''.join(map(str, number))

assert 0 == f_alu(number)
assert 0 == f_reverse_engineered(number)

print(number)
