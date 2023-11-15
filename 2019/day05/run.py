#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip()
		return map(int, line.split(','))

from functools import partial
from inspect import signature

class IntcodeComputer:

	def __init__(self, data, input):
		self.data = list(data)
		self.input = list(input)
		self.output = []

	@staticmethod
	def call_fn(fn, args, parameter_modes):
		return fn(*[ eval_arg(a) for eval_arg, a in zip(parameter_modes, args) ])

	@staticmethod
	def num_of_args(fn):
		return len(signature(fn).parameters)

	def get_args(self, fn):
		n_args = self.num_of_args(fn)
		return self.data[self.ptr+1:self.ptr+1+n_args]

	def write_ins(self, fn):
		def ins(fn, parameter_modes):
			args = self.get_args(fn)
			out = self.data[self.ptr+1+len(args)]
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

	def ins(self, op, parameter_modes):
		return {
			1: self.write_ins(lambda a1, a2: a1 + a2),
			2: self.write_ins(lambda a1, a2: a1 * a2),
			3: self.write_ins(lambda: self.input.pop(0)),
			4: self.basic_ins(lambda a1: self.output.append(a1)),
			5: self.jump_ins(lambda a1, a2: a2 if a1 != 0 else None),
			6: self.jump_ins(lambda a1, a2: a2 if a1 == 0 else None),
			7: self.write_ins(lambda a1, a2: int(a1 < a2)),
			8: self.write_ins(lambda a1, a2: int(a1 == a2)),
		}[op](parameter_modes)

	def run(self):
		self.ptr = 0
		while self.data[self.ptr] != 99:
			op_with_pm = self.data[self.ptr]
			op = op_with_pm % 100
			imm = lambda x: x
			mem = lambda x: self.data[x]
			parameter_modes = [ imm if (op_with_pm // pow(10, n)) % 2 else mem for n in range(2, 5) ]
			self.ins(op, parameter_modes)
		assert all(x == 0 for x in self.output[:-1])
		return self.output[-1]


# Part One

c = IntcodeComputer(load_data('input.txt'), [1])
print(c.run())

# Part Two

c = IntcodeComputer(load_data('input.txt'), [5])
print(c.run())
