#! /usr/bin/env python3

import numpy as np

def load_all_tiles(filename):
	with open(filename, 'r') as f:
		tile_lines = []
		tile_id = None
		for line in f:
			line = line.strip()
			if line == '':
				if len(tile_lines) == 10:
					yield Tile(tile_id, tile_lines)
					tile_lines = []
					tile_id = None
			elif line.startswith('Tile'):
				tile_id = int(line.split(' ')[1].strip(':'))
			elif len(line) == 10:
				tile_lines.append(line)
	if len(tile_lines) == 10:
		yield Tile(tile_id, tile_lines)

class Tile:

	def __init__(self, tile_id, lines):
		self.tile_id = tile_id
		self.tile = self.parse_lines(lines)
		self.all_tiles = self.all_tile_rotations(self.tile)
		self.tile_borders = list(self.all_tile_borders(self.all_tiles))

	@staticmethod
	def parse_lines(lines):
		mat = []
		for line in lines:
			line = list(map(int, line.replace('#', '1').replace('.', '0')))
			mat.append(line)
		return np.array(mat, dtype=int)

	@staticmethod
	def all_tile_rotations(m):
		flipped = np.flip(m, axis=0)
		return [ np.rot90(m, n) for n in range(4) ] + [ np.rot90(flipped, n) for n in range(4) ]

	@staticmethod
	def all_tile_borders(all_tiles):
		for r in all_tiles:
			yield int(''.join(map(str, r[0])), 2)

# Part One

tiles = []
jar = {}
max_tiles_per_border = 0
for t in load_all_tiles('input.txt'):
	tiles.append(t)
	for b in t.tile_borders:
		if b in jar:
			jar[b].append(t)
		else:
			jar[b] = [t]
		if max_tiles_per_border < len(jar[b]):
			max_tiles_per_border = len(jar[b])

assert max_tiles_per_border == 2

corners = []

for t in tiles:
	num_non_connected_borders = 0
	for b in t.tile_borders:
		if len(jar[b]) == 1:
			num_non_connected_borders += 1
		elif len(jar[b]) == 2:
			pass
		else:
			raise Exception("oops")
	if num_non_connected_borders == 4:
		corners.append(t)

assert len(corners) == 4

prod = 1
for t in corners:
	prod *= t.tile_id
print("corners tile_id product", prod)

# Part Two

monster = Tile(None, [
	'..................#.',
	'#....##....##....###',
	'.#..#..#..#..#..#...',
])

class Puzzle:

	def __init__(self, size, tile_size):
		self.w, self.h = size
		self.tile_w, self.tile_h = tile_size
		# hard coded overlap == 1 pixel
		self.picture = np.zeros( (self.h * (self.tile_h-1) + 1, self.w * (self.tile_w-1) + 1), dtype=int )
		self.mask = np.zeros( self.picture.shape, dtype=int )

	def put(self, coords, t):
		x, y = coords
		px, py = x * (self.tile_w-1), y * (self.tile_h-1)
		tile_mask = self.mask[py:py+t.shape[0],px:px+t.shape[1]]
		tile_picture = self.picture[py:py+t.shape[0],px:px+t.shape[1]]
		eq = np.all(np.equal(np.multiply(t, tile_mask), tile_picture))
		if not eq:
			return False
		tile_mask[...] = 1
		tile_picture[...] = t
		return True

picture = Puzzle( (12, 12), (10, 10) )

# correct value [0..3] found with bruteforcing
first_corner_orientation_id = 2

picture.put( (0, 0), corners[0].all_tiles[first_corner_orientation_id][0:1,...] )

used_tiles = {}
for y in range(12):
	for x in range(12):
		found_tile = False
		for t in tiles:
			if id(t) in used_tiles:
				continue
			for oriented_tile in t.all_tiles:
				if picture.put( (x, y), oriented_tile ):
					used_tiles[id(t)] = True
					found_tile = True
					break
			if found_tile:
				break
		if not found_tile:
			raise Exception("Tile not found, try another first_corner_orientation_id value")

# remove right and bottom edges
sea = picture.picture[:-1,:-1]
# reshape so that there are +2 dimensions for tiles grid
sea = np.reshape(sea, (12, 9, 12, 9))
# remove left and top borders from each tile
sea = sea[:,1:,:,1:]
# reshape back to 2d
sea = np.reshape(sea, (8*12, 8*12))

def rolling_window_2d(a, window):
	shape = (a.shape[0] - window.shape[0] + 1,) + \
		(a.shape[1] - window.shape[1] + 1,) + \
		window.shape
	strides = a.strides + a.strides
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

before = np.sum(sea)

for oriented_sea in Tile.all_tile_rotations(sea):
	possible_monsters = rolling_window_2d(oriented_sea, monster.tile)
	detected_monsters = np.all(np.equal(monster.tile, np.multiply(possible_monsters, monster.tile)), axis=(2,3))
	for y in range(detected_monsters.shape[0]):
		for x in range(detected_monsters.shape[1]):
			if detected_monsters[y,x]:
				# since possible_monsters is a view of oriented_sea, changing it's contents directly changes oriented_sea
				# see Notes: https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html
				possible_monsters[y,x,...] *= (1 - monster.tile)
	after = np.sum(oriented_sea)
	if before != after:
		print(after)
		break
