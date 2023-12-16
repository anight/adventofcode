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
			g = constant_sum_iterator(n-1, s-i, t)
			feedback = None
			while True:
				try:
					r = g.send(feedback)
				except StopIteration:
					break
				feedback = yield (i,) + r
				if feedback != None:
#					print(f"{feedback=}")
					if t-n >= feedback:
						break

#def constant_sum_iterator2(n, s):
	
#	ranges = [ [ (1 if 0 < i < n-1 else 0),  for i in range(n):

@lru_cache
def arrangements(pattern, groups):
#	print(f"arrangements {pattern=}")
#	print(f"arrangements {groups=}")
	spaces = len(pattern) - sum(groups)
	if len(groups) == 0:
#		print(f"{int('#' not in pattern)=}")
		return int('#' not in pattern)
	if spaces < len(groups) - 1:
#		print("not enough spaces")
		return 0
#	ranges = [ range(0, spaces+1) ] + [ range(1, spaces+1) for _ in range(len(groups) - 1) ] + [ range(0, spaces+1) ]
	good = 0
#	reduced = []
#	print(f"{len(groups)+1=}")
#	print(f"{spaces=}")
	g = constant_sum_iterator(len(groups)+1, spaces, len(groups)+1)
#	g = constant_sum_iterator2(len(groups)+1, spaces)
	send_value = None
	while True:
		try:
			s = g.send(send_value)
		except StopIteration:
			break
#		print(s)
		assert sum(s) == spaces
		assert all( s[i] > 0 for i in range(1, len(groups)) )
		assert sum( groups + s ) == len(pattern)
		test_string = pattern
		for i, num in enumerate(groups):
			assert len(test_string) > 0
			if not match_string(test_string[:s[i]], '.' * s[i]):
#				send_value = i+1
				break
			test_string = test_string[s[i]:]
			if not match_string(test_string[:num], '#' * num):
#				send_value = i+1
				break
			test_string = test_string[num:]
		else:
			if match_string(test_string, '.' * s[-1]):
#				print("match")
				good += 1
				send_value = None
#				reduced.append(test_string)
	'''
	simplified = list(pattern)
	for i, ch in enumerate(pattern):
		if ch != '?':
			continue
		chars = set([ variant[i] for variant in reduced ])
		if len(chars) > 1:
			continue
		simplified[i] = list(chars)[0]
	simplified = ''.join(simplified)
	simplified_groups = list(groups)
	'''
#	print(f"{good=}")
	return good#, simplified

'''
total = 0

for pattern, groups in load_data('input.txt'):
	a = arrangements(pattern, groups)
#	print(pattern, groups, a)
	total += a

print(total)

exit()
'''

# Part Two

def subarrangements(patterns, groups):
#	print(">>>", len(patterns), "called", patterns, groups)
#	if len(groups) == 0:
#		yield int(all( '#' not in p for p in patterns ))
	if len(patterns) == 0:
#		print(">>>", len(patterns), f"ret1", f"{int(len(groups) == 0)=}", groups)
		yield int(len(groups) == 0)
	else:
#		if len(groups) == 0:
#			print("ret2", f"{int(all('#' not in pattern for pattren in pattrens))=}")
#			return int(all('#' not in pattern for pattren in patterns))
		pattern = patterns[0]
		for i in range(len(groups)+1):
			a = arrangements(pattern, groups[:i])
			if a != 0:
#				print(">>>", len(patterns), f"{a=}")
				for rest in subarrangements(patterns[1:], groups[i:]):
#					print(">>>", len(patterns), "ret0", rest)
					yield a * rest

def median(s, split_ch):
	median_ch = sorted([ (abs(i-len(s)/2), i) for i, ch in enumerate(s) if ch == split_ch ])[0][1]
	return median_ch

from math import factorial
import multiprocessing as mp
import time

def complex_arrangements(pattern, groups):
	skipped = 0
	started = time.time()
	if '.' in pattern:
#		print(pattern)
		subpatterns = [ p for p in pattern.split('.') if p != '' ]
		a = sum(subarrangements(subpatterns, groups))
	else:
#		print(pattern, groups)
		min_spaces = len(groups) - 1
		spaces = len(pattern) - sum(groups) - min_spaces
		buckets = len(groups) + 1
		if spaces < 0:
			return 0, 0, 0, 0
#		print(f"{min_spaces=}")
#		print(f"{spaces=}")
#		print(f"{buckets=}")
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
						a1, _, _, _ = complex_arrangements(pattern[:median_ch+1], groups[:i] + (j+1,))
						a2, _, _, _ = complex_arrangements(pattern[median_ch:], (g-j,) + groups[i+1:])
						a += a1 * a2
#					if combinations < 1e6:
#					a = arrangements(pattern, groups)
#						print(">>>>>>>>>>>>>>>>")
#					else:
#						print("skip")
#						a = 0
#						skipped += 1
		else:
			a = combinations
	elapsed = time.time() - started
	return a, skipped, pattern, elapsed

def worker_task(input_queue, output_queue):
	while True:
		task = input_queue.get()
		if task is None:
			break
		result = complex_arrangements(*task)
		output_queue.put(result)

total = 0
skipped = 0

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
	print(f"reading {tasks_enqueued} tasks")
	result = output_queue.get()
	num, sk, pattern, elapsed = result
	total += num
	skipped += sk
	print(elapsed, pattern, num, sk)
	tasks_enqueued -= 1

for _ in range(num_workers):
	input_queue.put(None)

for worker in workers:
	worker.join()

print(total)
print(f"{skipped=}")
