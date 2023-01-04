#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		monkeymap = []
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				break
			monkeymap.append(line)
		all_actions = f.readline().rstrip()
		return monkeymap, all_actions

from dataclasses import dataclass

monkeymap, all_actions = load_data('input.txt')

@dataclass
class Walker:
	x: int
	y: int
	direction: int

	def final_password(self):
		return 1000 * (self.y + 1) + 4 * (self.x + 1) + self.direction

	def L(self):
		self.direction = (self.direction + 3) % 4

	def R(self):
		self.direction = (self.direction + 1) % 4

	def F(self):
		direction, x, y = self.one_step_forward(self.direction, self.x, self.y)
		if monkeymap[y][x] != '#':
			self.x = x
			self.y = y
			self.direction = direction

	def action(self, value):
		if value == 'L':
			self.L()
		elif value == 'R':
			self.R()
		else:
			steps = int(value)
			for _ in range(steps):
				self.F()

	@staticmethod
	def actions(all_actions):
		res = ''
		for ch in all_actions:
			if len(res) > 0 and ch.isnumeric() != res[-1].isnumeric():
				yield res
				res = ''
			res += ch
		yield res

# Part One

class WalkerFlat(Walker):

	@staticmethod
	def one_step_forward(direction, x, y):
		if direction == 0:
			nx, ny = x + 1, y
			if nx == len(monkeymap[ny]):
				nx = len(monkeymap[ny]) - len(monkeymap[ny].lstrip(' '))
		elif direction == 1:
			nx, ny = x, y + 1
			if ny == len(monkeymap):
				ny = 0
			while nx >= len(monkeymap[ny]) or monkeymap[ny][nx] == ' ':
				ny += 1
				if ny == len(monkeymap):
					ny = 0
		elif direction == 2:
			nx, ny = x - 1, y
			if nx < 0 or monkeymap[ny][nx] == ' ':
				nx = len(monkeymap[ny])-1
		elif direction == 3:
			nx, ny = x, y - 1
			if ny < 0:
				ny = len(monkeymap) - 1
			while nx >= len(monkeymap[ny]) or monkeymap[ny][nx] == ' ':
				ny -= 1
				if ny < 0:
					ny = len(monkeymap) - 1
		return direction, nx, ny

w = WalkerFlat(monkeymap[0].index('.'), 0, 0)

for action in w.actions(all_actions):
	w.action(action)

print(w.final_password())

# Part Two

class Face:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def id(self):
		return (self.x, self.y)

	def edges(self):
		yield (self.x+1, self.y), (self.x+1, self.y+1), 0
		yield (self.x, self.y+1), (self.x+1, self.y+1), 1
		yield (self.x, self.y),   (self.x, self.y+1),   2
		yield (self.x, self.y),   (self.x+1, self.y),   3

class Walker3DFold(Walker):

	def __init__(self, *args, **kwargs):
		super(Walker3DFold, self).__init__(*args, **kwargs)
		self.create_3d_fold()

	def create_3d_fold(self):

		def all_cube_faces():
			for y in range(0, len(monkeymap), 50):
				for x in range(0, len(monkeymap[y]), 50):
					if monkeymap[y][x] != ' ':
						yield Face(x // 50, y // 50)

		# corners to edges map
		c2e = {}
		# edges to faces map
		e2f = {}

		for face in all_cube_faces():
			for f, t, d in face.edges():
				c2e[f] = c2e.get(f, set()) | set([(f, t)])
				c2e[t] = c2e.get(t, set()) | set([(t, f)])
				if (f, t) in e2f:
					e2f[(f, t)].append((d, face.id()))
				else:
					e2f[(f, t)] = [ (d, face.id()) ]

		while 0 < sum( 1 for faces in e2f.values() if len(faces) == 1 ):
			for f, t in e2f.keys():
				def merge(p):
					faces = set()
					g = []
					for e in c2e[p]:
						key = tuple(sorted(e))
						for f in e2f[key]:
							faces |= set([f[1]])
						n_faces = len(e2f[key])
						if n_faces == 1:
							g.append(e)
					if len(g) != 2 or len(faces) != 3:
						return False
					# merge edges of the merged corner
					c2e[g[0][1]] |= c2e[g[1][1]]
					c2e[g[1][1]] |= c2e[g[0][1]]
					# add missing faces to the merged edges
					a1 = e2f[tuple(sorted(g[0]))]
					a2 = e2f[tuple(sorted(g[1]))]
					a1.append(a2[0])
					a2.append(a1[0])
					return True
				if merge(f):
					break
				if merge(t):
					break

		def transition(x1, y1, d1, x2, y2, d2):
			# https://en.wikipedia.org/wiki/Rotation_matrix#Common_rotations
			rotm = ( (1, 0, 0, 1), (0, 1, -1, 0), (-1, 0, 0, -1), (0, -1, 1, 0) )
			angle = (4 + d1 - d2) % 4
			r = rotm[angle]
			# take one dot "from" and one dot "to"
			df = ( (50, 0), (49, 50), (-1, 49), (0, -1) )[d1]
			dt = ( (0, 0), (49, 0), (49, 49), (0, 49) )[d2]
			# and calculate a difference in coordinates
			c1 = x2 * 50 + dt[0] - (x1 * 50 + df[0]) * r[0] - (y1 * 50 + df[1]) * r[1]
			c2 = y2 * 50 + dt[1] - (x1 * 50 + df[0]) * r[2] - (y1 * 50 + df[1]) * r[3]
			return r[0], r[1], c1, r[2], r[3], c2, d2

		self.transitions = {}

		for (f, t), faces in e2f.items():
			(d1, f1), (d2, f2) = faces
			self.transitions[(*f1, d1)] = transition(f1[0], f1[1], d1, f2[0], f2[1], (d2+2)%4)
			self.transitions[(*f2, d2)] = transition(f2[0], f2[1], d2, f1[0], f1[1], (d1+2)%4)

	def one_step_forward(self, direction, x, y):
		nx, ny = {0: (x+1, y), 1: (x, y+1), 2: (x-1, y), 3: (x, y-1)}[direction]
		if (x // 50, y // 50) != (nx // 50, ny // 50):
			a1, b1, c1, a2, b2, c2, tdirection = self.transitions[ (x // 50, y // 50, direction) ]
			tx = a1 * nx + b1 * ny + c1
			ty = a2 * nx + b2 * ny + c2
			return tdirection, tx, ty
		return direction, nx, ny

w = Walker3DFold(monkeymap[0].index('.'), 0, 0)

for action in w.actions(all_actions):
	w.action(action)

print(w.final_password())
