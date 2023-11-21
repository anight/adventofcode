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

from floyd_warshall import Graph

c = IntcodeComputer(load_data('input.txt'), [])

g = Graph()

# None: unexplored
# 0: empty
# 1: wall
# 2: oxygen system
field = {(0, 0): 0}
unexplored = {}
x, y = 0, 0
g.add_node((0, 0))
oxygen = None

def all_neighbours(x, y):
	dx, dy = 1, 0
	for _ in range(4):
		yield x+dx, y+dy
		dx, dy = -dy, dx

def add_unexplored(x, y):
	for nx, ny in all_neighbours(x, y):
		key = (nx, ny)
		if key not in field:
			unexplored[key] = (x, y, nx-x, ny-y)

add_unexplored(x, y)

# 1. Find closest unexplored cell
# 2. Travel to there, update map on arrival
# 3. If found - break

while len(unexplored):
	unexplored_candidates = sorted([ (g.get_distance( (x, y), (tx, ty) ), (tx, ty, dx, dy) ) for tx, ty, dx, dy in unexplored.values() ])
#	print("unexplored_candidates", len(unexplored_candidates))
	assert len(unexplored_candidates) > 0
	key = unexplored_candidates[0][1]
	tx, ty, dx, dy = key

	def move(tx, ty, dx, dy):
#		print("moving", dx, dy)
		command = {(0, -1): 1, (0, 1): 2, (-1, 0): 3, (1, 0): 4}[(dx, dy)]
		c.input.append(command)
		r = c.run()
		if (tx+dx, ty+dy) in unexplored:
			del unexplored[(tx+dx, ty+dy)]
		return r

	if (tx, ty) != (x, y):
		shortest_path = g.shortest_path((x, y), (tx, ty))[1:]
#		print("shortest path between", x, y, "and", tx, ty, ":", shortest_path)
		while (x, y) != (tx, ty):
			to = shortest_path.pop(0)
			move(x, y, to[0]-x, to[1]-y)
			x, y = to

	r = move(tx, ty, dx, dy)

	if r == 0:
#		print("found wall at", tx+dx, ty+dy)
		field[(tx+dx, ty+dy)] = 1
		continue

	x, y = tx+dx, ty+dy
	field[(x, y)] = 0
	add_unexplored(x, y)
	g.add_node( (x, y) )

#	print("explored cell", x, y)

	for nx, ny in all_neighbours(x, y):
		key = (nx, ny)
		if key in field and field[key] != 1:
			g.update_distance( (x, y), key, 1 )

	g.update_distances_for_node( (x, y) )

	if r == 2 and oxygen is None:
#		print("found oxygen", x, y)
		oxygen = (x, y)

s = g.shortest_path((0, 0), oxygen)

print(len(s)-1)

# Part Two

next_oxygen = {}
field[oxygen] = 2

def add_next_oxygen(x, y, n):
	for nx, ny in all_neighbours(x, y):
		key = (nx, ny)
		if key in field and field[key] == 0:
			n[key] = None

add_next_oxygen(oxygen[0], oxygen[1], next_oxygen)

steps = 0
while len(next_oxygen) > 0:
	next_next_oxygen = {}
	for x, y in next_oxygen.keys():
		field[(x, y)] = 2
		add_next_oxygen(x, y, next_next_oxygen)
	next_oxygen = next_next_oxygen
	steps += 1

print(steps)
