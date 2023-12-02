#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			game_id = int(line.split(': ')[0].split(' ')[1])
			draws = []
			for draw in line.split(': ')[1].split('; '):
				items = draw.split(', ')
				draws.append({ item.split(' ')[1]: int(item.split(' ')[0]) for item in items })
			yield game_id, draws

# Part One

red, green, blue = 12, 13, 14

total = 0

for game_id, draws in load_data('input.txt'):
	possible = True
	for draw in draws:
		if draw.get('red', 0) > red:
			possible = False
			break
		if draw.get('green', 0) > green:
			possible = False
			break
		if draw.get('blue', 0) > blue:
			possible = False
			break
	if possible:
		total += game_id

print(total)

# Part Two

total = 0

for game_id, draws in load_data('input.txt'):
	max_seen = {}
	for draw in draws:
		max_seen['red'] = max(max_seen.get('red', 0), draw.get('red', 0))
		max_seen['green'] = max(max_seen.get('green', 0), draw.get('green', 0))
		max_seen['blue'] = max(max_seen.get('blue', 0), draw.get('blue', 0))
	total += max_seen['red'] * max_seen['green'] * max_seen['blue']

print(total)

