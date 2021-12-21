#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			command, n = line.split()
			yield command, int(n)
# Part One

h, d = 0, 0

for command, n in load_data('input.txt'):
	if command == 'forward':
		h += n
	elif command == 'down':
		d += n
	elif command == 'up':
		d -= n
	else:
		raise("oops")

print(h * d)

# Part Two

h, d, aim = 0, 0, 0

for command, n in load_data('input.txt'):
	if command == 'forward':
		h += n
		d += aim * n
	elif command == 'down':
		aim += n
	elif command == 'up':
		aim -= n
	else:
		raise("oops")

print(h * d)
