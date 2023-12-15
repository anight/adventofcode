#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		return f.readline().rstrip('\n').split(',')

# Part One

sequence = load_data('input.txt')

def hash(str):
	value = 0
	for ch in str:
		value += ord(ch)
		value *= 17
		value %= 256
	return value

total = sum( hash(str) for str in sequence )

print(total)

# Part Two

boxes = [ list() for _ in range(256) ]

for str in sequence:
	label = str.split('-')[0].split('=')[0]
	box_id = hash(label)
	is_set = '=' in str
	focal_length = int(str.split('=')[1]) if is_set else None
	if is_set:
		for i, (i_label, _) in enumerate(boxes[box_id]):
			if i_label == label:
				break
		else:
			boxes[box_id].append( (label, focal_length) )
			continue
		boxes[box_id][i] = (label, focal_length)
	else:
		for i, (i_label, _) in enumerate(boxes[box_id]):
			if i_label == label:
				break
		else:
			continue
		boxes[box_id].pop(i)

def focusing_power(box):
	return sum( (i + 1) * focal_length for i, (_, focal_length) in enumerate(box) )

total = sum( (i + 1) * focusing_power(box) for i, box in enumerate(boxes) )

print(total)

