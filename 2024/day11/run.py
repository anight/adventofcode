#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split()))

data = next(load_data('input.txt'))

# Part One

class Stones:
	def __init__(self, stones):
		self.stones = { s: 1 for s in stones }

	def blink(self):
		new_stones = {}
		def add(n, cnt):
			new_stones[n] = new_stones.get(n, 0) + cnt
		for n, cnt in self.stones.items():
			if n == 0:
				add(1, cnt)
			elif len(a := str(n)) % 2 == 0:
				add(int(a[:len(a)//2]), cnt)
				add(int(a[len(a)//2:]), cnt)
			else:
				add(n * 2024, cnt)
		self.stones = new_stones

	def count(self):
		return sum(self.stones.values())

s = Stones(data)

for _ in range(25):
	s.blink()

print(s.count())

# Part Two

for _ in range(50):
	s.blink()

print(s.count())
