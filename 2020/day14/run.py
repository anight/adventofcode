#! /usr/bin/env python3

from dataclasses import dataclass
from functools import cached_property

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line.split(' ')
			if line.startswith('mask = '):
				yield Mask(t[2])
			elif line.startswith('mem['):
				yield Mem(int(t[0][4:-1]), int(t[2]))

@dataclass
class Mask:
	value: str

	@cached_property
	def set_bits(self):
		return int(self.value.replace('X', '0'), 2)

	@cached_property
	def clear_bits(self):
		return int(self.value.replace('X', '1'), 2)

	def apply(self, value):
		return (value & self.clear_bits) | self.set_bits

	def apply_generate_floating(self, value):
		value |= self.set_bits
		floating = [ i for i in range(len(self.value)) if self.value[len(self.value)-1-i] == 'X' ]
		for bits in range(2**len(floating)):
			v = value
			for i in range(len(floating)):
				if 0 == bits & (1 << i):
					v &= ~(1 << floating[i])
				else:
					v |= (1 << floating[i])
			yield v

@dataclass
class Mem:
	addr: int
	value: int

# Part One

mem = {}
mask = None
for item in load_data('input.txt'):
	match item:
		case Mask() as m:
			mask = m
		case Mem() as m:
			mem[m.addr] = mask.apply(m.value)

print(sum(mem.values()))

# Part Two

mem = {}
mask = None
for item in load_data('input.txt'):
	match item:
		case Mask() as m:
			mask = m
		case Mem() as m:
			for addr in mask.apply_generate_floating(m.addr):
				mem[addr] = m.value

print(sum(mem.values()))
