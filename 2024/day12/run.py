#! /usr/bin/env python3

a = { x+1j*y: c for y, line in enumerate(open('input.txt').read().splitlines()) for x, c in enumerate(line) }

# Part One

regions = {}
n_regions = 0

for c, plot in a.items():
	if c in regions:
		continue
	def find(c, plot, region_id):
		if c in regions:
			return
		if a.get(c, '') != plot:
			return
		regions[c] = region_id
		for d in range(4):
			find(c + 1j ** d, plot, region_id)
	find(c, plot, n_regions)
	n_regions += 1

def edges(region_id):
	edges = set()
	for c, v in regions.items():
		if v != region_id:
			continue
		for d in range(4):
			n = c + 1j ** d
			if regions.get(n, -1) != region_id:
				edges.add( (c, 1j ** d) )
	return edges

def perimeter(region_id):
	return len(edges(region_id))

def area(region_id):
	return sum( 1 for v in regions.values() if v == region_id )

result = sum( area(region_id) * perimeter(region_id) for region_id in range(n_regions) )

print(result)

# Part Two

def sides(region_id):
	pieces = edges(region_id)

	def find_side(c, d):
		nonlocal pieces
		side = (c, c, d)
		while True:
			new_left = side[0] - 1j * d
			new_right = side[1] + 1j * d
			new_side = ( new_left if (new_left, d) in pieces else side[0],
				new_right if (new_right, d) in pieces else side[1], d )
			if new_side == side:
				return side
			side = new_side

	sides = [ find_side(c, d) for c, d in pieces ]
	return len(set(sides))

result = sum( area(region_id) * sides(region_id) for region_id in range(n_regions) )

print(result)
