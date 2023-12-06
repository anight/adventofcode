#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		times = f.readline().rstrip('\n').split()[1:]
		distances = f.readline().rstrip('\n').split()[1:]
		return list(map(int, times)), list(map(int, distances))

# Part One

times, distances = load_data('input.txt')

total = 1

def distance(total_time, button_time):
	speed = button_time
	return (total_time - button_time) * speed

for t, record_distance in zip(times, distances):
	variants = sum( 1 for b in range(t+1) if distance(t, b) > record_distance )
	total *= variants

print(total)

# Part Two

time = int(''.join(map(str, times)))
record_distance = int(''.join(map(str, distances)))

def search(low, high, f):
	while high - low > 1:
		mid = (high + low) // 2
		test = f(mid)
		if test > 0:
			low = mid
		else:
			high = mid
	return high

def lower_bound(x):
	if distance(time, x) <= record_distance:
		return 1
	if distance(time, x-1) > record_distance:
		return -1
	return 0

def upper_bound(x):
	if distance(time, x) > record_distance:
		return 1
	if distance(time, x-1) <= record_distance:
		return -1
	return 0

value_from = search(0, time, lower_bound)
value_to = search(value_from, time, upper_bound)

print(value_to - value_from)
