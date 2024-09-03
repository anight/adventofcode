#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Set
import numpy as np

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield list(map(int, line.split(',')))

coords = np.array(list(load_data('input.txt')))

# Part One

@dataclass
class Constellation:
	stars: Set[int]

proximity = 3
radius = 12
n_dim = coords.shape[1]

neighbours_coords = np.mgrid[ [slice(-proximity, proximity+1, 1)] * n_dim ]
neighbours_in_proximity = np.where(np.sum(np.abs(neighbours_coords), axis=0) <= proximity)

coords += radius

m = np.full([2 * radius] * n_dim, -1, dtype=int)

constellations = []

for i in range(coords.shape[0]):
	constellations.append(Constellation({i}))
	c = coords[i]
	m[*c] = i

	def neighbours(coord):
		box = m[ tuple( slice(c-proximity, c+proximity+1) for c in coord ) ]
		return [ x for x in box[neighbours_in_proximity] if x != -1 ]

	stars = set()
	for n in neighbours(c):
		stars |= constellations[n].stars

	m[tuple(coords[list(stars)].transpose())] = i
	constellations[i].stars = stars

print(len(set(m[np.where(m != -1)])))

