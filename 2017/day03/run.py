#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return int(line)

# Part One

from math import sqrt

num = load_data('input.txt')

def coord(n):
	sq = int((sqrt(n-1) - 1) // 2)
	side = 2 * sq + 2
	linear = n - (2 * sq + 1) ** 2 - 1
	side_index = linear % side
	d = sq + abs(side_index - sq) + 1
	return d

print(coord(num))

# Part Two

result = 0
memory = {0: 1}
p, d = 0, 1

while result <= num:
	def mem_sum(cell):
		return sum( memory.get(cell + 1j**d, 0) + memory.get(cell + (1+1j) * 1j**d, 0) for d in range(4) )
	cell = p + d
	result = mem_sum(cell)
	memory[cell] = result
	left = d * -1j
	if cell + left not in memory:
		d = left
	p = cell

print(result)
