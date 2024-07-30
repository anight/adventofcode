#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in sorted(f.readlines()):
			line = line.rstrip('\n')
			ts = line[1:17]
			msg = line[19:]
			minute = int(ts[-2:])
			if msg.startswith('Guard'):
				guard_id = int(msg.split(' ')[1][1:])
				yield minute, "guard", guard_id
			elif msg.startswith('falls'):
				yield minute, "falls"
			elif msg.startswith('wakes'):
				yield minute, "wakes"

# Part One

import numpy as np

guard_stats = {}
guard_id = None
falls_asleep = None

for item in load_data('input.txt'):
	minute = item[0]
	event = item[1]
	if event == "guard":
		guard_id = item[2]
		if guard_id not in guard_stats:
			guard_stats[guard_id] = np.zeros(60, dtype=int)
	elif event == "falls":
		falls_asleep = minute
	elif event == "wakes":
		guard_stats[guard_id][falls_asleep:minute] += 1
		falls_asleep = None

_, guard_id = sorted( [ (np.sum(stats), guard_id) for guard_id, stats in guard_stats.items() ], reverse=True)[0]

minute = np.argmax(guard_stats[guard_id])

print(guard_id * minute)


# Part Two

max_guard_id = None
max_minute = None
max_sleep = 0

for guard_id, stats in guard_stats.items():
	argmax = np.argmax(stats)
	if max_sleep < stats[argmax]:
		max_guard_id = guard_id
		max_minute = argmax
		max_sleep = stats[argmax]

print(max_guard_id * max_minute)
