#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield tuple(map(int, line.split(',')))

def neighbours(x, y, z):
	yield x+1, y, z
	yield x-1, y, z
	yield x, y+1, z
	yield x, y-1, z
	yield x, y, z+1
	yield x, y, z-1

# Part One

cubes = {}
total = 0
for x, y, z in load_data('input.txt'):
	total += 6 - 2 * sum( n in cubes for n in neighbours(x, y, z) )
	cubes[ (x, y, z) ] = None

print(total)

# Part Two

minx, maxx = float('inf'), -float('inf')
miny, maxy = float('inf'), -float('inf')
minz, maxz = float('inf'), -float('inf')
for x, y, z in cubes.keys():
	minx, maxx = min(minx, x), max(maxx, x)
	miny, maxy = min(miny, y), max(maxy, y)
	minz, maxz = min(minz, z), max(maxz, z)

def isolated(x, y, z):
	visited = { (x, y, z): None }
	lookup = { c: None for c in neighbours(x, y, z) if c not in cubes }
	while len(lookup) > 0:
		x, y, z = next(iter(lookup))
		del lookup[ (x, y, z) ]
		visited[ (x, y, z) ] = None
		if x in (minx, maxx) or y in (miny, maxy) or z in (minz, maxz):
			return False
		lookup |= { c: None for c in neighbours(x, y, z) if c not in cubes and c not in visited and c not in lookup }
	return True

cubes_isolated = []
isolated_faces = 0
for x in range(minx+1, maxx):
	for y in range(miny+1, maxy):
		for z in range(minz+1, maxz):
			if (x, y, z) not in cubes:
				if isolated(x, y, z):
					isolated_faces += sum( n in cubes for n in neighbours(x, y, z) )

print(total - isolated_faces)
