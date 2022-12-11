#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line.split(' ')
			if 1 == len(t):
				yield t[0], None
			else:
				yield t[0], int(t[1])

# Part One

total = 0
cycle = 1
regX = 1
for op, arg in load_data('input.txt'):
	def tick():
		global cycle, regX, total
		if 0 == (cycle-20) % 40:
			total += cycle * regX
		cycle += 1
	if op == 'noop':
		tick()
	elif op == 'addx':
		tick()
		tick()
		regX += arg

print(total)

# Part Two

import numpy as np
crt = np.zeros([240], dtype=int)
cycle = 0
regX = 1
for op, arg in load_data('input.txt'):
	def tick():
		global crt, cycle, regX
		if abs((cycle%40)-regX) <= 1:
			crt[cycle] = 1
		cycle += 1
	if op == 'noop':
		tick()
	elif op == 'addx':
		tick()
		tick()
		regX += arg

for line in crt.reshape((6, 40)):
	print(''.join(map(str, line)).replace('1', '#').replace('0', '.'))

