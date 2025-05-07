#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

input = next(load_data('input.txt'))

nums = list(map(int, input.split(',')))

# Part One

class Circle:
	def __init__(self, n):
		self.n = n
		self.lst = list(range(n))
		self.current = 0
		self.skip_size = 0

	def reverse(self, length):
		s, e = self.current, (self.current+length-1) % self.n
		for _ in range(length//2):
			self.lst[s], self.lst[e] = self.lst[e], self.lst[s]
			s = (s+1) % self.n
			e = (e-1) % self.n

	def run(self, lengths):
		for length in lengths:
			self.reverse(length)
			self.current = (self.current + length + self.skip_size) % self.n
			self.skip_size += 1

	def dense_hash(self):
		for i in range(0, 256, 16):
			n = 0
			for j in range(i, i+16):
				n ^= self.lst[j]
			yield n

	def hex_hash(self):
		return ''.join(f'{n:02x}' for n in self.dense_hash())

c = Circle(256)

c.run(nums)

print(c.lst[0] * c.lst[1])

# Part Two

c = Circle(256)

nums = list(map(ord, input)) + [17, 31, 73, 47, 23]

for _ in range(64):
	c.run(nums)

print(c.hex_hash())
