#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line

def calc_id(seat):
	row = int(seat[:7].replace('F', '0').replace('B', '1'), 2)
	col = int(seat[7:].replace('L', '0').replace('R', '1'), 2)
	id = row * 8 + col
	return id

# Part One

highest_id = 0
for seat in load_data('input.txt'):
	id = calc_id(seat)
	if highest_id < id:
		highest_id = id

print(highest_id)

# Part Two
all_seats = dict( (id, True) for id in range(highest_id+1) )
for seat in load_data('input.txt'):
	id = calc_id(seat)
	del all_seats[id]

for id in range(highest_id):
	if id in all_seats:
		del all_seats[id]
	else:
		break

print(next(iter(all_seats)))
