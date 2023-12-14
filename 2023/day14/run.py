#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(line)

# Part One

import numpy as np

a = np.array(list(load_data('input.txt')))

def roll_north(a):
	while True:
		moved = 0
		for y, x in zip(*np.where(a[1:,...] == 'O')):
			y += 1
			if a[y-1,x] == '.':
				a[y-1,x] = 'O'
				a[y,x] = '.'
				moved += 1
		if moved == 0:
			break

def total_load(a):
	return sum(a.shape[0] - y for y, x in zip(*np.where(a == 'O')) )

roll_north(a)

print(total_load(a))

# Part Two

a = np.array(list(load_data('input.txt')))

def roll_west(a):
	while True:
		moved = 0
		for y, x in zip(*np.where(a[...,1:] == 'O')):
			x += 1
			if a[y,x-1] == '.':
				a[y,x-1] = 'O'
				a[y,x] = '.'
				moved += 1
		if moved == 0:
			break

def roll_south(a):
	while True:
		moved = 0
		for y, x in zip(*np.where(a[:-1,...] == 'O')):
			if a[y+1,x] == '.':
				a[y+1,x] = 'O'
				a[y,x] = '.'
				moved += 1
		if moved == 0:
			break

def roll_east(a):
	while True:
		moved = 0
		for y, x in zip(*np.where(a[...,:-1] == 'O')):
			if a[y,x+1] == '.':
				a[y,x+1] = 'O'
				a[y,x] = '.'
				moved += 1
		if moved == 0:
			break

history = {}

rolls = []

for i in range(1000):
	roll_north(a)
	roll_west(a)
	roll_south(a)
	roll_east(a)
	rolls.append(total_load(a))

	key = ''.join(''.join(line) for line in a)

	if key in history:
		period = i - history[key]
		break
	else:
		history[key] = i
else:
	raise Exception("oops")

print(rolls[i - period + (1_000_000_000 - i - 1) % period])
