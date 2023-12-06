#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		maps = {}
		current_map = []
		for line in f:
			line = line.rstrip('\n')
			if line.startswith('seeds:'):
				seeds = list(map(int, line.split(': ')[1].split()))
			elif line.endswith(':'):
				map_from, map_to = line[:-len(" map:")].split('-to-')
			elif line == '':
				if len(current_map) > 0:
					maps[ (map_from, map_to) ] = current_map
					current_map = []
			else:
				current_map.append( list(map(int, line.split())) )
		if len(current_map) > 0:
			maps[ (map_from, map_to) ] = current_map
		return seeds, maps

# Part One

seeds, maps = load_data('input.txt')

min_location = float('inf')

for value in seeds:
	key = 'seed'
	while key != 'location':
		next_key = [ map_to for map_from, map_to in maps.keys() if map_from == key ][0]
		ranges = maps[ (key, next_key) ]
		for dst, src, r in ranges:
			if src <= value < src + r:
				value = dst + value - src
				break
		key = next_key
	min_location = min(min_location, value)

print(min_location)

# Part Two

# pip3 install portion
import portion as P

min_location = float('inf')

for i in range(0, len(seeds), 2):
	src, r = seeds[i:i+2]
	ranges_from = P.closed(src, src + r - 1)
	key = 'seed'
	while key != 'location':
		translated = P.empty()
		next_key = [ map_to for map_from, map_to in maps.keys() if map_from == key ][0]
		ranges = maps[ (key, next_key) ]
		for dst, src, r in ranges:
			intersection = ranges_from & P.closed(src, src + r - 1)
			for interval in intersection:
				translated |= P.closed(dst + interval.lower - src, dst + interval.upper - src)
				ranges_from -= interval
		translated |= ranges_from
		key = next_key
		ranges_from = translated
	min_location = min(min_location, ranges_from.lower)

print(min_location)
