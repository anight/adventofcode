#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().strip()
		numbers = list(map(int, line.split(',')))
		return numbers

# Part One

numbers = load_data('input.txt')

def oneday(numbers):
	newnumbers = []
	new = 0
	for n in numbers:
		n -= 1
		if n == -1:
			n = 6
			new += 1
		newnumbers.append(n)
	return newnumbers + [8] * new

for _ in range(80):
	numbers = oneday(numbers)

print(len(numbers))

# Part Two

numbers = load_data('input.txt')

by_age = [0] * 9

for n in numbers:
	by_age[n] += 1

def oneday2(by_age):
	by_age = list(by_age)
	forked = by_age.pop(0)
	by_age[6] += forked
	by_age.append(forked)
	return by_age

for _ in range(256):
	by_age = oneday2(by_age)

sum = 0
for n in by_age:
	sum += n

print(sum)

