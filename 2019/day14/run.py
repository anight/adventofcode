#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			ingredients, target = line.rstrip().split(' => ')
			ingredients = ingredients.split(', ')
			yield target.split(' ')[1], (int(target.split(' ')[0]), [ (i.split(' ')[1], int(i.split(' ')[0])) for i in ingredients ])

reactions = dict(load_data('input.txt'))

def ore_needed(target, n, leftovers=None):
	if leftovers is None:
		leftovers = dict()
	out, ingredients = reactions[target]
	k = 1
	saved = leftovers.get(target, 0)
	if n <= saved:
		leftovers[target] -= n
		return 0
	k = (n - saved) // out
	if k * out < n - saved:
		k += 1
	ore = 0
	leftovers[target] = k * out - n + saved
	for i, amount in ingredients:
		if i == 'ORE':
			ore += k * amount
		else:
			ore += ore_needed(i, k * amount, leftovers)
	return ore

# Part One

print(ore_needed('FUEL', 1))

# Part Two

target_ore = 1e12
low, high = None, None
fuel = 1
while True:
	if high is None:
		ore = ore_needed('FUEL', fuel)
		if ore <= target_ore:
			low = fuel
			fuel *= 2
		else:
			high = fuel
		continue

	if low + 1 == high:
		break
	fuel = (high + low) // 2
	ore = ore_needed('FUEL', fuel)
	if ore <= target_ore:
		low = fuel
	else:
		high = fuel

print(low)
