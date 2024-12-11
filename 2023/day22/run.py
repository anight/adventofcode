#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split('~')
			yield Brick(map(int, t[0].split(',')), map(int, t[1].split(',')))

# Part One

class Brick:
	def __init__(self, f, t):
		self.f = tuple(f)
		self.t = tuple(t)
		assert self.t >= self.f
		assert 1 >= sum([self.t[0] > self.f[0], self.t[1] > self.f[1], self.t[2] > self.f[2]])
		self.under = set()
		self.over = set()

	def cubes(self):
		fx, fy, fz = self.f
		tx, ty, tz = self.t
		while True:
			yield fx, fy, fz
			if (fx, fy, fz) == (tx, ty, tz):
				break
			fx += tx > fx
			fy += ty > fy
			fz += tz > fz

	def bottom_cubes(self):
		fx, fy, fz = self.f
		tx, ty, tz = self.t

		if fz != tz:
			yield self.f
		else:
			yield from self.cubes()

	def top_cubes(self):
		fx, fy, fz = self.f
		tx, ty, tz = self.t

		if fz != tz:
			yield self.t
		else:
			yield from self.cubes()

	def z_distance_under(self, brick):
		tops = {}
		for x, y, z in brick.top_cubes():
			tops[(x, y)] = z
		for x, y, z in self.bottom_cubes():
			if (x, y) in tops:
				return z - tops[(x, y)] - 1
		raise Exception("oops")

	def z_distance_over(self, brick):
		return brick.z_distance_under(self)

	def fall(self, by):
		self.f = (self.f[0], self.f[1], self.f[2] - by)
		self.t = (self.t[0], self.t[1], self.t[2] - by)

	def would_fall_without(self, bricks):
		return all( self.z_distance_under(b) > 0 for b in self.under - bricks )

	def is_disintegratable(self):
		return all( not b.would_fall_without(set([self])) for b in self.over )

	def __repr__(self):
		return f"{self.f}~{self.t}"

TOP = 0

bricks = list(load_data('input.txt'))
stack = {}

for brick in bricks:
	for cube in brick.cubes():
		stack[cube] = brick
		TOP = max(TOP, cube[2])

for brick in bricks:
	for cx, cy, cz in brick.bottom_cubes():
		for z in range(cz-1, 0, -1):
			if (cx, cy, z) in stack:
				break
		else:
			continue
		brick.under.add(stack[(cx, cy, z)])
	for cx, cy, cz in brick.top_cubes():
		for z in range(cz+1, TOP+1):
			if (cx, cy, z) in stack:
				break
		else:
			continue
		brick.over.add(stack[(cx, cy, z)])

def all_fall():
	moved = 0

	for brick in bricks:
		fall_by = 0
		if len(brick.under) == 0:
			fall_by = next(iter(brick.bottom_cubes()))[2] - 1
		else:
			fall_by = min( brick.z_distance_under(u) for u in brick.under )
		if fall_by == 0:
			continue

		brick.fall(fall_by)
		moved += 1

	return moved

while all_fall():
	pass

disintegratable = [ brick for brick in bricks if brick.is_disintegratable() ]

print(len(disintegratable))


# Part Two

total = 0

for brick in bricks:
	fallen = set([brick])

	while True:

		def test(fallen):
			to_test = set([ b for brick in fallen for b in brick.over ]) - fallen
			add = set()
			for b in to_test:
				if b.would_fall_without(fallen):
					add.add(b)
			return add

		add = test(fallen)
		if len(add) == 0:
			break

		fallen |= add

	total += len(fallen - set([brick]))

print(total)
