#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		return list(map(int, f.readline().rstrip()))

import numpy as np

values = np.array(load_data('input.txt'), dtype=np.int32)

# Part One

def seq(period, i):
	return 1-abs((((i+1) // period) % 4)-1)

m = []
for mul in range(1, len(values)+1):
	a = [ seq(mul, i) for i in range(values.size) ]
	m.append(a)
m = np.array(m, dtype=np.int32)

def fft(values):
	return np.abs(np.dot(m, values)) % 10

for _ in range(100):
	values = fft(values)

print(''.join(map(str, values[:8])))

# Part Two

values = load_data('input.txt') * 10000

skip = int(''.join(map(str, values[:7])))
assert skip >= len(values) // 2

tail = values[skip:]
for _ in range(100):
	def new_tail(tail):
		ret = []
		acc = 0
		for i in range(len(tail)-1, -1, -1):
			acc = (acc + tail[i]) % 10
			ret.append(acc)
		return list(reversed(ret))
	tail = new_tail(tail)

print(''.join(map(str, tail[:8])))
