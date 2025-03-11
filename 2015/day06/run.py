#! /usr/bin/env python3

def load_data(filename):
	def c(t):
		return tuple(map(int, t.split(',')))
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' ')
			if t[1] == 'on':
				yield 'on', c(t[2]), c(t[4])
			elif t[1] == 'off':
				yield 'off', c(t[2]), c(t[4])
			else:
				yield 'toggle', c(t[1]), c(t[3])

import numpy as np

# Part One

a = np.zeros([1000, 1000], dtype=bool)

for c, f, t in load_data('input.txt'):
	if c == 'on':
		a[f[0]:t[0]+1,f[1]:t[1]+1] = True
	elif c == 'off':
		a[f[0]:t[0]+1,f[1]:t[1]+1] = False
	else:
		a[f[0]:t[0]+1,f[1]:t[1]+1] = 1 - a[f[0]:t[0]+1,f[1]:t[1]+1]

print(np.sum(a))

# Part Two

a = np.zeros([1000, 1000], dtype=int)

for c, f, t in load_data('input.txt'):
	if c == 'on':
		a[f[0]:t[0]+1,f[1]:t[1]+1] += 1
	elif c == 'off':
		a[f[0]:t[0]+1,f[1]:t[1]+1] -= 1
		a = np.clip(a, a_min=0, a_max=None)
	else:
		a[f[0]:t[0]+1,f[1]:t[1]+1] += 2

print(np.sum(a))
