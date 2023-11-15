#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip()
		return map(int, line.split(','))

from operator import add, mul
from functools import partial
from inspect import signature

class IntcodeComputer:

	def __init__(self, data, input):
		self.data = dict(enumerate(data))
		self.input = list(input)
		self.instructions = {
			1: self.write_ins(add),
			2: self.write_ins(mul),
			3: self.write_ins(lambda: self.input.pop(0)),
			4: self.basic_ins(lambda a1: self.output.append(a1)),
			5: self.jump_ins(lambda a1, a2: a2 if a1 != 0 else None),
			6: self.jump_ins(lambda a1, a2: a2 if a1 == 0 else None),
			7: self.write_ins(lambda a1, a2: int(a1 < a2)),
			8: self.write_ins(lambda a1, a2: int(a1 == a2)),
			9: self.basic_ins(self.relative_base_add),
		}

	def relative_base_add(self, arg):
		self.relative_base += arg

	@staticmethod
	def call_fn(fn, args, parameter_modes):
		return fn(*[ eval_arg(a) for eval_arg, a in zip(parameter_modes, args) ])

	@staticmethod
	def num_of_args(fn):
		return len(signature(fn).parameters)

	def get_args(self, fn):
		n_args = self.num_of_args(fn)
		return [ self.data[x] for x in range(self.ptr+1, self.ptr+1+n_args) ]

	def write_ins(self, fn):
		def ins(fn, parameter_modes):
			args = self.get_args(fn)
			out = self.data[self.ptr+1+len(args)]
			if parameter_modes[len(args)] == self.rel:
				out += self.relative_base
			self.data[out] = self.call_fn(fn, args, parameter_modes)
			self.ptr += 1+len(args)+1
		return partial(ins, fn)

	def basic_ins(self, fn):
		def ins(fn, parameter_modes):
			args = self.get_args(fn)
			self.call_fn(fn, args, parameter_modes)
			self.ptr += 1+len(args)
		return partial(ins, fn)

	def jump_ins(self, fn):
		def ins(fn, parameter_modes):
			args = self.get_args(fn)
			new_ptr = self.call_fn(fn, args, parameter_modes)
			if new_ptr is None:
				self.ptr += 1+len(args)
			else:
				self.ptr = new_ptr
		return partial(ins, fn)

	def imm(self, x):
		return x

	def mem(self, x):
		return self.data.get(x, 0)

	def rel(self, x):
		return self.data.get(self.relative_base + x, 0)

	def run(self):
		self.output = []
		self.relative_base = 0
		self.ptr = 0
		while self.data[self.ptr] != 99:
			op_with_pm = self.data[self.ptr]
			op = op_with_pm % 100
			parameter_modes = [ (self.mem, self.imm, self.rel)[int(f"{op_with_pm:05d}"[::-1][n])] for n in range(2, 5) ]
			self.instructions[op](parameter_modes)
		if len(self.output):
			return self.output[-1]
		return None


# Part One

c = IntcodeComputer(load_data('input.txt'), [1])
print(c.run())

# Part Two

c = IntcodeComputer(load_data('input.txt'), [2])
print(c.run())
