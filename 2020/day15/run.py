#! /usr/bin/env python3

input = "20,9,11,0,1,2"

spoken = list(map(int, input.split(',')))
last = { n: i for i, n in enumerate(spoken[:-1]) }

def play(limit):
	while len(spoken) < limit:
		number = spoken[-1]
		if number in last:
			spoken.append(len(spoken) - 1 - last[number])
		else:
			spoken.append(0)
		last[number] = len(spoken) - 2

# Part One

play(2020)
print(spoken[2020-1])

# Part Two

play(30_000_000)
print(spoken[30_000_000-1])
