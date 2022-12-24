#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			name, value = line.split(': ')
			if value.isnumeric():
				yield name, int(value)
			else:
				ops = value.split()
				operators = {"+": add, "-": sub, "*": mul, "/": floordiv}
				yield name, (operators[ops[1]], ops[0], ops[2])

from operator import add, sub, mul, floordiv, eq

monkeys = dict(load_data('input.txt'))

# Part One

def value(node):
	v = monkeys[node]
	if type(v) is int:
		return v
	op, arg1, arg2 = v
	return op(value(arg1), value(arg2))
print(value('root'))

# Part Two

class Unknown: pass
monkeys['humn'] = Unknown
monkeys['root'] = (eq, *monkeys['root'][1:])

def value2(node, res=None):
	v = monkeys[node]
	if type(v) is int:
		return v
	if v is Unknown:
		if res is not None:
			print(res)
			return res
		return Unknown
	op, arg1, arg2 = v
	res1 = value2(arg1)
	res2 = value2(arg2)
	if (res1 is Unknown) != (res2 is Unknown):
		if res is None:
			return Unknown
		if res1 is Unknown:
			def recover_arg1(op, res, res2):
				return {add: sub, sub: add, mul: floordiv, floordiv: mul, eq: lambda a, b: b}[op](res, res2)
			res1 = recover_arg1(op, res, res2)
			value2(arg1, res1)
		else:
			def recover_arg2(op, res, res1):
				return {add: sub, sub: lambda a, b: sub(b, a), mul: floordiv, floordiv: lambda a, b: floordiv(b, a), eq: lambda a, b: b}[op](res, res1)
			res2 = recover_arg2(op, res, res1)
			value2(arg2, res2)
	return op(res1, res2)

value2('root', True)
