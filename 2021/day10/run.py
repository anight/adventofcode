#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line

# Part One

def calc_invalid_score(line):
	state = []
	for c in line:
		if c in '({[<':
			state.append(c)
			continue
		if c in ')}]>':
			op = state.pop()
			if c != {'{': '}', '(': ')', '[': ']', '<': '>'}[op]:
				return {')': 3, ']': 57, '}': 1197, '>': 25137}[c]
			continue
		raise "oops"
	return 0

invalid_score = 0

for line in load_data('input.txt'):
	invalid_score += calc_invalid_score(line)

print(invalid_score)

# Part Two

def calc_incomplete_score(line):
	state = []
	for c in line:
		if c in '({[<':
			state.append(c)
			continue
		if c in ')}]>':
			op = state.pop()
			if c != {'{': '}', '(': ')', '[': ']', '<': '>'}[op]:
				return 0
			continue
		raise "oops"
	ret = 0
	for c in state[::-1]:
		ret *= 5
		ret += {'{': 3, '(': 1, '[': 2, '<': 4}[c]
	return ret

scores = []

for line in load_data('input.txt'):
	score = calc_incomplete_score(line)
	if score == 0:
		continue
	scores.append(score)

scores = sorted(scores)

print(scores[len(scores)//2])

