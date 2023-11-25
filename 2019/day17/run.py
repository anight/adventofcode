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

	def input_line(self, s):
		for ch in s:
			self.input.append(ord(ch))
		self.input.append(10)

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
		while self.data[self.ptr] != 99 and len(self.output) == 0:
			op_with_pm = self.data[self.ptr]
			op = op_with_pm % 100
			parameter_modes = [ (self.mem, self.imm, self.rel)[int(f"{op_with_pm:05d}"[::-1][n])] for n in range(2, 5) ]
			self.instructions[op](parameter_modes)
		if len(self.output):
			return self.output[-1]
		return None


# Part One

import numpy as np

c = IntcodeComputer(load_data('input.txt'), [])

field = []
line = []

while True:
	ch = c.run()
	if ch is None:
		break
	if ch == 10:
		if len(line):
			field.append(line)
		line = []
	else:
		if chr(ch) in '<>v^':
			robot_dxdy = {ord('^'): (0, -1), ord('>'): (1, 0), ord('v'): (0, 1), ord('<'): (-1, 0)}[ch]
			robot_xy = (len(line), len(field))
		line.append({ord('#'): 1}.get(ch, 0))
	# print(chr(ch), end='')

field = np.array(field, dtype=int)

def rolling_window(a, window):
	shape = np.array(a.shape, dtype=int) - np.array(window.shape, dtype=int) + 1
	shape = tuple(shape) + window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

padded = np.pad(field, 1, mode='constant')
kernel_intersection = np.array([ [0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)
rolled = rolling_window(padded, kernel_intersection)
intersections = np.sum(rolled == kernel_intersection, axis=(2, 3)) == 9
result = np.dot(*np.where(intersections))

print(result)

# Part Two

c = IntcodeComputer(load_data('input.txt'), [])
c.data[0] = 2

# Scan all the moves

def all_moves(robot_xy, robot_dxdy):
	x, y = robot_xy[0]+1, robot_xy[1]+1
	dx, dy = robot_dxdy

	forward = 0
	last_turn = None
	while True:
		if padded[y+dy, x+dx] == 1:
			forward += 1
			x += dx
			y += dy
			continue
		if forward > 0:
			yield (last_turn, forward)
			forward = 0
		if padded[y+dx, x-dy] == 1:
			last_turn = 'R'
			dx, dy = -dy, dx
			continue
		if padded[y-dx, x+dy] == 1:
			last_turn = 'L'
			dx, dy = dy, -dx
			continue
		if forward > 0:
			yield (last_turn, forward)
		break

moves = list(all_moves(robot_xy, robot_dxdy))

# Build dictionary

from collections import defaultdict

subsequences = defaultdict(int)

# We are limiting our dictionary:
# 1. by frequency ( freq>1 )
# 2. by length ( 5>=length>=2 )
# Not 100% sure this is correct way to go

for i in range(len(moves)):
	for j in range(i+1, len(moves)):
		if j+1 - i > 5:
			continue
		subseq = tuple(moves[i:j+1])
		subsequences[subseq] += 1

dictionary = [ list(k) for k, v in subsequences.items() if v > 1 ]

# Try to build main movement routine

from itertools import product

for words in product(dictionary, repeat=3):
	# Max 10 substitutions
	i = 0
	commands = []
	while i < len(moves):
		for cmd, word in zip('ABC', words):
			if moves[i:i+len(word)] == word:
				commands.append(cmd)
				break
		else:
			break
		i += len(word)
	if i == len(moves) and len(commands) <= 10:
		break
else:
	raise Exception("not found")

commands = ','.join(commands)
words = [ ','.join(f"{t[0]},{t[1]}" for t in w) for w in words ]

c.input_line(commands)
for w in words:
	c.input_line(w)
c.input_line('n')

while True:
	ch = c.run()
	if ch is None:
		break
	if ch > 255:
		break

print(ch)
