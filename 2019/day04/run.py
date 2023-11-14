#! /usr/bin/env python3

f, t = 156218, 652527

# Part One

def meets_the_criteria(n):
	n = str(n)
	two_adjacent_found = False
	for i in range(5):
		if n[i] == n[i+1]:
			two_adjacent_found = True
		if n[i] > n[i+1]:
			return False
	return two_adjacent_found

result = sum(meets_the_criteria(n) for n in range(f, t+1))

print(result)

# Part Two

def meets_the_criteria(n):
	n = str(n)
	two_adjacent_found = False
	last, cnt = None, 0
	for c in n:
		if last is not None:
			if c < last:
				return False
			if c == last:
				cnt += 1
			else:
				if cnt == 2:
					two_adjacent_found = True
				cnt = 1
		else:
			cnt = 1
		last = c
	return two_adjacent_found or cnt == 2

result = sum(meets_the_criteria(n) for n in range(f, t+1))

print(result)

