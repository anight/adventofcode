#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line[len("Step ")], line[len("Step . must be finished before step ")]

# Part One

reqs = list(load_data('input.txt'))

deps = {}

for must_be_finished_before, step in reqs:
	if step not in deps:
		deps[step] = set([ must_be_finished_before ])
	else:
		deps[step] |= set([ must_be_finished_before ])

	if must_be_finished_before not in deps:
		deps[must_be_finished_before] = set()

steps = ''

while set(deps.keys()) - set(steps):
	found = set()
	for k, v in deps.items():
		if k in steps:
			continue
		if v - set(steps):
			continue
		found |= set(k)
	steps += sorted(found)[0]

print(steps)

# Part Two

max_workers = 5
delay = lambda c: 61 + ord(c) - ord('A')
in_workers = lambda: set( c for _, c in workers )
steps = ''
workers = []
seconds = 0

while True:
	# Unload from workers
	for i, (s, c) in enumerate(list(workers)):
		if s == seconds:
			steps += c
			workers.remove( (s, c) )
	# Check if we are done
	if not set(deps.keys()) - set(steps):
		break
	# Find steps we can take
	found = set()
	for k, v in deps.items():
		if k in steps:
			continue
		if k in in_workers():
			continue
		if v - set(steps):
			continue
		found |= set(k)
	# Load workers as much as we can
	while len(workers) < max_workers and found:
		c = list(found)[0]
		workers.append( (seconds + delay(c), c) )
		found -= set([c])
	seconds += 1

print(seconds)

