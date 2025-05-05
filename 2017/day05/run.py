#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield int(line)

# Part One

instructions = list(load_data('input.txt'))

ptr = 0
steps = 0

while ptr < len(instructions):
	jump = instructions[ptr]
	instructions[ptr] += 1
	ptr += jump
	steps += 1

print(steps)

# Part Two

instructions = list(load_data('input.txt'))

ptr = 0
steps = 0

while ptr < len(instructions):
	jump = instructions[ptr]
	if jump >= 3:
		instructions[ptr] -= 1
	else:
		instructions[ptr] += 1
	ptr += jump
	steps += 1

print(steps)
