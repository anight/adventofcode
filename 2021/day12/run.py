#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line.split('-')

# Part One

connections = {}

for f, t in load_data('input.txt'):
	if f not in connections:
		connections[f] = [t]
	else:
		connections[f].append(t)
	if t not in connections:
		connections[t] = [f]
	else:
		connections[t].append(f)

paths = []
search_paths = [('start',)]

while len(search_paths) > 0:
	p = search_paths.pop()
	for next_step in connections[p[-1]]:
		if next_step == next_step.lower():
			if next_step in p:
				continue
		path = p + (next_step,)
		if next_step == 'end':
			paths.append(path)
		else:
			search_paths.append(path)

print(len(paths))

# Part Two

paths = []
search_paths = [(False, ('start',))]

while len(search_paths) > 0:
	single_small_was_visited_twice, p = search_paths.pop()
	for next_step in connections[p[-1]]:
		if next_step == 'start':
			continue
		if next_step == 'end':
			paths.append(path)
			continue
		next_step_single_small_was_visited_twice = single_small_was_visited_twice
		if next_step == next_step.lower():
			if next_step in p:
				if single_small_was_visited_twice:
					continue
				next_step_single_small_was_visited_twice = True
		path = p + (next_step,)
		search_paths.append((next_step_single_small_was_visited_twice, path))

print(len(paths))

