#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			t = line.split()
			onoff = 1 if t[0] == "on" else 0
			c = t[1].split(',')
			x = c[0].split('=')[1].split('..')
			y = c[1].split('=')[1].split('..')
			z = c[2].split('=')[1].split('..')
			yield onoff, (int(x[0]), int(x[1]), int(y[0]), int(y[1]), int(z[0]), int(z[1]))

# Part One

import numpy as np

a = np.zeros([101]*3, dtype=int)

for t, (xf, xt, yf, yt, zf, zt) in load_data('input.txt'):
	if np.any(np.abs( (xf, xt, yf, yt, zf, zt) ) > 50):
		continue
	a[zf+50:zt+1+50,yf+50:yt+1+50,xf+50:xt+1+50] = t

print(np.sum(a))


# Part Two

class DiscreteVolumeStorage(object):
	def __init__(self):
		self.storage = []

	def set(self, new_aabb, v):
		i = 0
		while i < len(self.storage):
			aabb = list(self.storage[i])
			skip = False
			cuts = []
			for j, ((start, stop), (new_start, new_stop)) in enumerate(zip(aabb, new_aabb)):
				if stop <= new_start or new_stop <= start:
					skip = True
				elif stop > new_stop or start < new_start:
					if start < new_start < stop:
						cuts.append(aabb[:j] + [ (start, new_start) ] + aabb[j+1:])
					if start < new_stop < stop:
						cuts.append(aabb[:j] + [ (new_stop, stop) ] + aabb[j+1:])
					aabb[j] = ( max(start, new_start), min(stop, new_stop) )
			if skip:
				i += 1
				continue

			if len(cuts) > 0:
				self.storage += cuts

			self.storage.pop(i)

		if v:
			self.storage.append(new_aabb)

	def volume(self):
		total = 0
		for aabb in self.storage:
			volume = 1
			for start, stop in aabb:
				volume *= (stop - start)
			total += volume
		return total

	def __setitem__(self, k, v):
		aabb = []
		for s in k:
			assert type(s) is slice
			assert s.stop > s.start
			assert s.step is None or s.step == 1
			aabb.append( (s.start, s.stop) )
		self.set(aabb, v)

dvs = DiscreteVolumeStorage()

for t, (xf, xt, yf, yt, zf, zt) in load_data('input.txt'):
	dvs[zf:zt+1,yf:yt+1,xf:xt+1] = t

print(dvs.volume())

