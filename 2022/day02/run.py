#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield line.split()

# Part One

total = 0
for peer, me in load_data('input.txt'):
	def outcome(me, peer):
		match me + peer:
			case "YA" | "ZB" | "XC":
				return 6
			case "XA" | "YB" | "ZC":
				return 3
			case _:
				return 0
	score = {"X": 1, "Y": 2, "Z": 3}[me]
	score += outcome(me, peer)
	total += score

print(total)

# Part Two

total = 0
for peer, outcome in load_data('input.txt'):
	def me(peer, outcome):
		match outcome + peer:
			case "XB" | "YA" | "ZC":
				return 1
			case "XC" | "YB" | "ZA":
				return 2
			case _:
				return 3
	score = me(peer, outcome)
	score += {"X": 0, "Y": 3, "Z": 6}[outcome]
	total += score

print(total)
