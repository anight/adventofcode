#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip()
		ts = int(line)
		line = f.readline().rstrip()
		buses = [ int(x) if x.isnumeric() else x for x in line.split(',') ]
		return ts, buses

# Part One

ts, buses = load_data('input.txt')
best_ts = None
best_bus = None
for bus in buses:
	if bus == 'x':
		continue
	next_ts = (ts + bus - 1) // bus * bus
	if best_ts is None or best_ts > next_ts:
		best_ts = next_ts
		best_bus = bus

print(best_bus * (best_ts - ts))

# Part Two

# Okay, let's bring in some black magic and prime numbers properties

period = None
offset = 0
for i, bus in enumerate(buses):
	if bus == 'x':
		continue
	if period is None:
		period = bus
		continue
	c = 1
	while (period * c + i + offset) % bus != 0:
		c += 1
	offset += period * c
	period *= bus

print(offset)
