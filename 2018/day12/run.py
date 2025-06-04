#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		initial = f.readline().rstrip('\n').split(': ')[1]
		m = {}
		f.readline()
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' => ')
			m[t[0]] = t[1]
	return initial, m

# Part One

plants, m = load_data('input.txt')
offset = 0
assert m['.....'] == '.'

def one_step(plants, offset):
	plants = '....' + plants + '....'
	ret = ''
	for i in range(len(plants) - 4):
		sub = plants[i:i+5]
		ret += m[sub]
	while ret[0] == '.':
		ret = ret[1:]
		offset += 1
	ret = ret.rstrip('.')
	return ret, offset-2

def score(plants, offset):
	return sum( (1 if ch == '#' else 0) * i for i, ch in enumerate(plants, offset) )

for _ in range(20):
	plants, offset = one_step(plants, offset)

print(score(plants, offset))


# Part Two

steps_to_go = 50_000_000_000 - 20

prev_plants = None
while prev_plants != plants:
	prev_plants = plants
	prev_offset = offset
	plants, offset = one_step(plants, offset)
	steps_to_go -= 1

offset += (offset - prev_offset) * steps_to_go

print(score(plants, offset))
