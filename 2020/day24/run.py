#! /usr/bin/env python3

def load_all_tiles(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			coord = next_coord((0, 0), line)
			yield coord

def next_coord(coord, line):
	if line == '':
		return coord
	if coord[0] % 2 == 0:
		if line.startswith('se'):
			return next_coord((coord[0]+1, coord[1]), line[2:])
		if line.startswith('e'):
			return next_coord((coord[0], coord[1]+1), line[1:])
		if line.startswith('ne'):
			return next_coord((coord[0]-1, coord[1]), line[2:])
		if line.startswith('nw'):
			return next_coord((coord[0]-1, coord[1]-1), line[2:])
		if line.startswith('w'):
			return next_coord((coord[0], coord[1]-1), line[1:])
		if line.startswith('sw'):
			return next_coord((coord[0]+1, coord[1]-1), line[2:])
	else:
		if line.startswith('se'):
			return next_coord((coord[0]+1, coord[1]+1), line[2:])
		if line.startswith('e'):
			return next_coord((coord[0], coord[1]+1), line[1:])
		if line.startswith('ne'):
			return next_coord((coord[0]-1, coord[1]+1), line[2:])
		if line.startswith('nw'):
			return next_coord((coord[0]-1, coord[1]), line[2:])
		if line.startswith('w'):
			return next_coord((coord[0], coord[1]-1), line[1:])
		if line.startswith('sw'):
			return next_coord((coord[0]+1, coord[1]), line[2:])
	raise Exception("can't decode \"{}\"".format(line))

def all_neighbours(coord):
	for direction in ('se', 'e', 'ne', 'nw', 'w', 'sw'):
		yield next_coord(coord, direction)

def next_state(black_tiles):
	next_black_tiles = {}
	checked_white = {}
	for coord in black_tiles.keys():
		num_black_neighbours = 0
		for neighbour_coord in all_neighbours(coord):
			if neighbour_coord in black_tiles:
				num_black_neighbours += 1
			else:
				if neighbour_coord not in checked_white:
					checked_white[neighbour_coord] = True
					num_black_neighbours_to_white = 0
					for neighbour_white_coord in all_neighbours(neighbour_coord):
						if neighbour_white_coord in black_tiles:
							num_black_neighbours_to_white += 1
					if num_black_neighbours_to_white == 2:
						next_black_tiles[neighbour_coord] = True
		if num_black_neighbours == 0 or num_black_neighbours > 2:
			pass
		else:
			next_black_tiles[coord] = True
	return next_black_tiles

# A test
black_tiles = {}
for coords in load_all_tiles('test.txt'):
	if coords in black_tiles:
		del black_tiles[coords]
	else:
		black_tiles[coords] = True

assert 10 == len(black_tiles)

# Part One
black_tiles = {}
for coords in load_all_tiles('input.txt'):
	if coords in black_tiles:
		del black_tiles[coords]
	else:
		black_tiles[coords] = True

print(len(black_tiles))

# Part Two
for _ in range(100):
	black_tiles = next_state(black_tiles)

print(len(black_tiles))
