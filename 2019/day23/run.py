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
		self.relative_base = 0
		self.ptr = 0
		self.output = []
		self.instructions = {
			1: self.write_ins(add),
			2: self.write_ins(mul),
			3: self.write_ins(self.read_input),
			4: self.basic_ins(lambda a1: self.output.append(a1)),
			5: self.jump_ins(lambda a1, a2: a2 if a1 != 0 else None),
			6: self.jump_ins(lambda a1, a2: a2 if a1 == 0 else None),
			7: self.write_ins(lambda a1, a2: int(a1 < a2)),
			8: self.write_ins(lambda a1, a2: int(a1 == a2)),
			9: self.basic_ins(self.relative_base_add),
		}

	def input_line(self, s):
		for ch in s:
			self.input.append(ord(ch))
		self.input.append(10)

	def read_input(self):
		if len(self.input):
			self.read_empty = 0
			return self.input.pop(0)
		self.read_empty += 1
		return -1

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

	def step(self):
		op_with_pm = self.data[self.ptr]
		op = op_with_pm % 100
		parameter_modes = [ (self.mem, self.imm, self.rel)[int(f"{op_with_pm:05d}"[::-1][n])] for n in range(2, 5) ]
		self.instructions[op](parameter_modes)

	def run(self):
		self.output = []
		while self.data[self.ptr] != 99 and len(self.output) == 0:
			self.step()
		if len(self.output):
			return self.output[-1]
		return None


# Part One

class NetworkComputer(IntcodeComputer):

	def __init__(self, address):
		self.address = address
		super(NetworkComputer, self).__init__(load_data('input.txt'), [address])

	def one_step(self):
		self.step()
		if len(self.output) == 3:
			address, x, y = self.output
			send(address, [x, y])
			del self.output[:]

computers = [ NetworkComputer(i) for i in range(50) ]
nat = []

def send(address, packet):
	if address == 255:
		nat[:] = packet
	else:
		computers[address].input.extend(packet)

while len(nat) == 0:
	for c in computers:
		c.one_step()
		if len(nat) != 0:
			break

print(nat[1])

# Part Two

last_y = None
result = None
while result is None:
	for c in computers:
		c.one_step()
		network_idle = all( len(c.input) == 0 and c.read_empty >= 1 for c in computers )
		if network_idle and len(nat):
			send(0, nat)
			if last_y is not None:
				if last_y == nat[1]:
					result = last_y
					break
			last_y = nat[1]

print(result)
