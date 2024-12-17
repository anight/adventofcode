#! /usr/bin/env python3.12

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			c = line.split(' ')
			yield c[0], tuple(map(int, c[1].split(',')))

# Part One

from functools import lru_cache

def match_string(pattern, test_string):
	assert len(pattern) == len(test_string)
	for a, b in zip(pattern, test_string):
		if a == '?':
			continue
		if a != b:
			return False
	return True

def constant_sum_iterator(n, s, t):
	if n == 1:
		yield (s,)
	else:
		for i in range(0 if n == t else 1, s+1):
			for r in constant_sum_iterator(n-1, s-i, t):
				yield (i,) + r

@lru_cache
def arrangements(pattern, groups):
	spaces = len(pattern) - sum(groups)
	if len(groups) == 0:
		return int('#' not in pattern)
	if spaces < len(groups) - 1:
		return 0
	good = 0
	for s in constant_sum_iterator(len(groups)+1, spaces, len(groups)+1):
		assert sum(s) == spaces
		assert all( s[i] > 0 for i in range(1, len(groups)) )
		assert sum( groups + s ) == len(pattern)
		test_string = pattern
		for i, num in enumerate(groups):
			assert len(test_string) > 0
			if not match_string(test_string[:s[i]], '.' * s[i]):
				break
			test_string = test_string[s[i]:]
			if not match_string(test_string[:num], '#' * num):
				break
			test_string = test_string[num:]
		else:
			if match_string(test_string, '.' * s[-1]):
				good += 1
	return good

total = sum( arrangements(pattern, groups) for pattern, groups in load_data('input.txt') )

print(total)

# Part Two

def subarrangements(patterns, groups):
	if len(patterns) == 0:
		yield int(len(groups) == 0)
	else:
		pattern = patterns[0]
		for i in range(len(groups)+1):
			a = arrangements(pattern, groups[:i])
			if a != 0:
				for rest in subarrangements(patterns[1:], groups[i:]):
					yield a * rest

def median(s, split_ch):
	median_ch = sorted([ (abs(i-len(s)/2), i) for i, ch in enumerate(s) if ch == split_ch ])[0][1]
	return median_ch

from math import factorial
import multiprocessing as mp

def complex_arrangements(pattern, groups):
	if '.' in pattern:
		subpatterns = tuple([ p for p in pattern.split('.') if p != '' ])
		a = sum(subarrangements(subpatterns, groups))
	else:
		min_spaces = len(groups) - 1
		spaces = len(pattern) - sum(groups) - min_spaces
		buckets = len(groups) + 1
		if spaces < 0:
			return 0
		combinations = int(factorial(spaces + buckets - 1) / ( factorial(buckets - 1) * factorial(spaces) ))
		if '#' in pattern:
			if '#' not in pattern[1:-1]:
				a = arrangements(pattern, groups)
			else:
				a = 0
				median_ch = median(pattern, '#')
				for i in range(len(groups)):
					g = groups[i]
					for j in range(g):
						a1 = complex_arrangements(pattern[:median_ch+1], groups[:i] + (j+1,))
						a2 = complex_arrangements(pattern[median_ch:], (g-j,) + groups[i+1:])
						a += a1 * a2
		else:
			a = combinations
	return a

def worker_task(input_queue, output_queue):
	while True:
		task = input_queue.get()
		if task is None:
			break
		result = complex_arrangements(*task)
		output_queue.put(result)

total = 0

num_workers = 16

input_queue = mp.Queue()
output_queue = mp.Queue()

workers = []
for _ in range(num_workers):
	worker = mp.Process(target=worker_task, args=(input_queue, output_queue))
	worker.start()
	workers.append(worker)

tasks_enqueued = 0

for pattern, groups in load_data('input.txt'):
	pattern = '?'.join([pattern] * 5)
	groups = groups * 5
	input_queue.put( (pattern, groups) )
	tasks_enqueued += 1

while tasks_enqueued > 0:
	result = output_queue.get()
	total += result
	tasks_enqueued -= 1

for _ in range(num_workers):
	input_queue.put(None)

for worker in workers:
	worker.join()

print(total)
