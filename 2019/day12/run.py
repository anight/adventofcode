#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			tokens = line.rstrip()[1:-1].split(', ')
			yield [ int(t.split('=')[1]) for t in tokens ]

import numpy as np
from itertools import permutations

# Part One

pos = np.array(list(load_data('input.txt')), dtype=int)
vel = np.zeros_like(pos)

def one_step(pos, vel):
	first, second = tuple(zip(*permutations(range(pos.shape[0]), 2)))
	gravity = np.sum(np.sign(pos[(second,)] - pos[(first,)]).reshape((pos.shape[0], pos.shape[0]-1, -1)), axis=1)
	vel += gravity
	pos += vel

for steps in range(1000):
	one_step(pos, vel)

total_energy = np.sum(np.sum(np.abs(pos), axis=1) * np.sum(np.abs(vel), axis=1))
print(total_energy)

# Part Two

pos = np.array(list(load_data('input.txt')), dtype=int)
vel = np.zeros_like(pos)

initial_pos = np.copy(pos)
initial_vel = np.copy(vel)
steps = 0
periods = {}

while True:
	one_step(pos, vel)
	steps += 1
	per_component_match_initial = np.logical_and(np.all(pos == initial_pos, axis=0), np.all(vel == initial_vel, axis=0))
	if any(per_component_match_initial):
		component = np.argmax(per_component_match_initial)
		if component in periods:
			continue
		periods[component] = steps
		if len(periods) == 3:
			break

print(np.lcm.reduce(list(periods.values())))
