#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' ')
			if t[1] in ('AND', 'OR'):
				yield t[1], t[4], t[0], t[2]
			elif t[1][1:] == 'SHIFT':
				yield t[1], t[4], t[0], t[2]
			elif t[0] == 'NOT':
				yield t[0], t[3], t[1]
			elif t[1] == '->':
				yield 'LOAD', t[2], t[0]
			else:
				raise Exception("unexpected")

# Part One

values = {}

def value(a):
	if a[0].isdigit():
		return int(a)
	else:
		if a not in values:
			values[a] = eval(wires[a])
		return values[a]

def op_and(a, b):
	return value(a) & value(b)

def op_or(a, b):
	return value(a) | value(b)

def op_not(a):
	return 0xffff ^ value(a)

def op_load(a):
	return value(a)

def op_rshift(a, b):
	return 0xffff & (value(a) >> value(b))

def op_lshift(a, b):
	return 0xffff & (value(a) << value(b))

wires = {}

for op in load_data('input.txt'):
	c, d = op[:2]
	args = op[2:]
	wires[d] = (globals()[f'op_{c.lower()}'], *args)

def eval(args):
	op, *args = args
	return op(*args)

value_a = eval(wires['a'])

print(value_a)

# Part Two

values = {}

wires['b'] = (op_load, str(value_a))

value_a = eval(wires['a'])

print(value_a)
