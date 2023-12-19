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

from discrete_volume_storage import DiscreteVolumeStorage

dvs = DiscreteVolumeStorage()

for t, (xf, xt, yf, yt, zf, zt) in load_data('input.txt'):
	dvs[zf:zt+1,yf:yt+1,xf:xt+1] = t

print(dvs.volume())

