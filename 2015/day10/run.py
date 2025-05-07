#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return line

# Part One

data = load_data('input.txt')

def expand(data):
	ret = ''
	last = None
	cnt = 0
	for digit in data:
		if last != digit:
			if last is not None:
				ret += str(cnt) + last
			last = digit
			cnt = 1
		else:
			cnt += 1
	if last is not None:
		ret += str(cnt) + last
	return ret

times = 40

for _ in range(times):
	data = expand(data)

print(len(data))

# Part Two

data = load_data('input.txt')

times = 50

for _ in range(times):
	data = expand(data)

print(len(data))
