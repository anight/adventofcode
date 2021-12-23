#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		beacons = []
		for line in f:
			line = line.strip()
			if line.startswith('---'):
				scanner_id = int(line[len('--- scanner '):-len(' ---')])
			elif line == '':
				yield scanner_id, beacons
				beacons = []
			else:
				coords = tuple(map(int, line.split(',')))
				beacons.append(coords)
		if len(beacons) > 0:
			yield scanner_id, beacons

# Part One

import numpy as np

class Scanner(object):
	def __init__(self, scanner_id, beacons):
		self.scanner_id = scanner_id
		self.scanners = [ (0, 0, 0) ]
		self.beacons = np.array(beacons, dtype=int)
		self.beacons_with_distances = []
		self.update_distances()

	def update_distances(self):
		self.beacons_with_distances = [ list() for _ in range(len(self.beacons)) ]
		for ai in range(0, self.beacons.shape[0]-1):
			for bi in range(ai+1, self.beacons.shape[0]):
				d = tuple(sorted(np.abs(self.beacons[ai] - self.beacons[bi])))
				self.beacons_with_distances[ai].append(d)
				self.beacons_with_distances[bi].append(d)
		for i in range(len(self.beacons_with_distances)):
			self.beacons_with_distances[i] = set(self.beacons_with_distances[i])

	def try_merge(self, s):
		common_beacons = []
		for i, a in enumerate(self.beacons_with_distances):
			best = None
			for j, b in enumerate(s.beacons_with_distances):
				n = len(a.intersection(b))
				if best is None:
					best = (n, i, j)
				else:
					if best[0] < n:
						best = (n, i, j)
			if best[0] >= 11:
				common_beacons.append(best)
		if len(common_beacons) < 12:
			return False

		# So here we have got at least 12 beacons each with 11 inter-distances noisy-matched

		m, disp = self.calc_orientation_and_displacement(
			np.array([ (self.beacons[i], s.beacons[j]) for _, i, j in common_beacons], dtype=int)
		)

		new_beacons = []

		for beacon in s.beacons @ m + disp:
			if np.any(np.all(beacon == self.beacons, axis=1)):
				...
			else:
				# Now check that beacon not in the scan zone of all the scanners of the space

				if not np.all(np.any(np.abs(self.scanners - beacon) > 1000, axis=1)):
					print("false positive merge")
					return False
				new_beacons.append(beacon)

		self.beacons = np.vstack((self.beacons, new_beacons))
		self.scanners.append( tuple(disp) )
		self.update_distances()

		return True

	def calc_orientation_and_displacement(self, common):
		a, b = common[:,0,:], common[:,1,:]
		# First two beacons is enough to detect orientation and displacement
		ax = a[0][0] - a[1][0]
		ay = a[0][1] - a[1][1]
		az = a[0][2] - a[1][2]
		bx = b[0][0] - b[1][0]
		by = b[0][1] - b[1][1]
		bz = b[0][2] - b[1][2]
		def c(n, m):
			if abs(n) == abs(m):
				if n == -m:
					return -1
				else:
					return 1
			return 0
		m = np.array([
			[c(ax, bx), c(ay, bx), c(az, bx)],
			[c(ax, by), c(ay, by), c(az, by)],
			[c(ax, bz), c(ay, bz), c(az, bz)]
		], dtype=int)
		b = b @ m
		disp = a[0,:] - b[0,:]
		b += disp
		assert np.all(a == b)
		return m, disp

scanners = []

for scanner_id, beacons in load_data('input.txt'):
	scanners.append(Scanner(scanner_id, beacons))

space = scanners.pop(0)

while len(scanners) > 0:
	for s in list(scanners):
		if space.try_merge(s):
			scanners.remove(s)

print(len(space.beacons))

# Part Two

from itertools import combinations

max_distance = None

for a, b in combinations(space.scanners, 2):
	distance = np.sum(np.abs(np.array(a, dtype=int) - np.array(b, dtype=int)))
	if max_distance is None:
		max_distance = distance
	else:
		if max_distance < distance:
			max_distance = distance

print(max_distance)
