#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

class Computer:
	def __init__(self, instructions):
		self.instructions = [ self.parse(ins) for ins in instructions ]
		self.reset()

	def reset(self):
		self.regs = {"a": 0, "b": 0, "c": 0, "d": 0}
		self.pc = 0

	def parse(self, ins):
		t = ins.split(' ')
		try:
			t[1] = int(t[1])
		except ValueError:
			pass
		try:
			t[2] = int(t[2])
		except (IndexError, ValueError):
			pass
		t[0] = getattr(self, f'op_{t[0]}')
		return tuple(t)

	def op_cpy(self, op, reg):
		if type(op) is int:
			value = op
		else:
			value = self.regs[op]
		self.regs[reg] = value
		self.pc += 1

	def op_jnz(self, op, offset):
		if type(op) is int:
			value = op
		else:
			value = self.regs[op]
		if value != 0:
			self.pc += offset
		else:
			self.pc += 1

	def op_inc(self, reg):
		self.regs[reg] += 1
		self.pc += 1

	def op_dec(self, reg):
		self.regs[reg] -= 1
		self.pc += 1

	def run(self):
		while self.pc < len(self.instructions):
			fn, *args = self.instructions[self.pc]
			fn(*args)

# Part One

c = Computer(load_data('input.txt'))
c.run()

print(c.regs["a"])

# Part Two

c.reset()
c.regs["c"] = 1
c.run()

print(c.regs["a"])
