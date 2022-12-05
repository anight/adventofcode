#! /usr/bin/env python3

from dataclasses import dataclass

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			if '[' in line:
				yield StackLine(line[1::4])
			elif line.startswith('move'):
				t = line.split(' ')
				yield MoveLine(int(t[1]), int(t[3]), int(t[5]))

@dataclass
class StackLine:
	crates: str

	def iterate(self):
		for i, crate in enumerate(self.crates, 1):
			if crate != ' ':
				yield i, crate

@dataclass
class MoveLine:
	cnt: int
	from_crate: int
	to_crate: int

class CrateMover:
	def __init__(self, load_data):
		self.stacks = dict()
		self.load_data = load_data

	def move(self, cnt, from_crate, to_crate):
		crates = self.stacks[from_crate][-cnt:]
		self.stacks[from_crate] = self.stacks[from_crate][:-cnt]
		self.stacks[to_crate] += self.order_crates(crates)

	def update_stack(self, i, crate):
		if i not in self.stacks:
			self.stacks[i] = list()
		self.stacks[i].insert(0, crate)

	def execute(self):
		for command in self.load_data:
			match command:
				case StackLine() as stack:
					for i, crate in stack.iterate():
						self.update_stack(i, crate)
				case MoveLine() as move:
					self.move(move.cnt, move.from_crate, move.to_crate)

	def __repr__(self):
		return ''.join(self.stacks[i][-1] for i in sorted(self.stacks.keys()))

class CrateMover9000(CrateMover):
	def order_crates(self, crates):
		return reversed(crates)

class CrateMover9001(CrateMover):
	def order_crates(self, crates):
		return crates

# Part One

crate_mover = CrateMover9000(load_data('input.txt'))
crate_mover.execute()
print(crate_mover)

# Part Two

crate_mover = CrateMover9001(load_data('input.txt'))
crate_mover.execute()
print(crate_mover)
