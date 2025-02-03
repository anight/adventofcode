#! /usr/bin/env python3

def load_data(filename):
	values = {}
	connections = {}
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if ': ' in line:
				t = line.split(': ')
				values[t[0]] = int(t[1])
			elif ' -> ' in line:
				t = line.split(' ')
				connections[t[4]] = ({'AND': and_, 'OR': or_, 'XOR': xor}[t[1]], t[0], t[2])
	return values, connections

from operator import and_, or_, xor

values, connections = load_data('input.txt')

# Part One

def evaluate(name):
	if name in values:
		return values[name]
	op, a1, a2 = connections[name]
	v1 = evaluate(a1)
	v2 = evaluate(a2)
	return op(v1, v2)

result = 0

def all_outputs():
	for i in range(len(connections)):
		output = f'z{i:02d}'
		if output not in connections:
			break
		yield i, output

for i, output in all_outputs():
	bit = evaluate(output)
	result |= (bit << i)

print(result)

# Part Two

found = []

# Check if any xor1 gate is connected directly to z output

def is_xor1(op, a1, a2):
	if a1 > a2:
		a1, a2 = a2, a1
	return op is xor and a1[0] == 'x' and a2[0] == 'y' and a1[1:] == a2[1:]

_, xor1 = zip(*sorted( (v[1][1:], k) for k, v in connections.items() if is_xor1(*v) ))

for net in xor1:
	if net[0] == 'z' and net != 'z00':
		found.append(net)

# Check if any and1 gate is connected directly to z output

def is_and1(op, a1, a2):
	if a1 > a2:
		a1, a2 = a2, a1
	return op is and_ and a1[0] == 'x' and a2[0] == 'y' and a1[1:] == a2[1:]

_, and1 = zip(*sorted( (v[1][1:], k) for k, v in connections.items() if is_and1(*v) ))

for net in and1:
	if net[0] == 'z':
		found.append(net)

# Check if any or1 gate is connected directly to z output

for k, (op, _, _) in connections.items():
	if op is or_:
		if net[0] == 'z' and net != 'z45':
			found.append(net)

# Draw the rest of fucking owl

def valid_and2_output(i, k):
	if i == 0:
		return True
	return 1 == sum( 1 for op, a1, a2 in connections.values() if op is or_ and (k == a1 or k == a2) )

carry = [and1[0]]
xor2 = [None]
and2 = [None]

for i, output in all_outputs():
	if i == 0 or i == 45:
		continue

	# find xor2
	for k, (op, a1, a2) in connections.items():
		if op is not xor:
			continue
		if k in xor1:
			continue
		result = 0
		result += (k == output)
		result += (carry[i-1] in (a1, a2))
		result += (xor1[i] in (a1, a2))
		if result < 2:
			continue
		if result == 2:
			if k != output:
				found.append(k)
			elif carry[i-1] not in (a1, a2):
				found.append(carry[i-1])
			elif xor1[i] not in (a1, a2):
				found.append(xor1[i])
		xor2.append(k)
		break
	else:
		raise Exception("not found")

	# find and2
	for k, (op, a1, a2) in connections.items():
		if op is not and_:
			continue
		if k in and1:
			continue
		result = 0
		result += valid_and2_output(i, k)
		result += (carry[i-1] in (a1, a2))
		result += (xor1[i] in (a1, a2))
		if result < 2:
			continue
		if result == 2:
			if not valid_and2_output(i, k):
				found.append(k)
			elif carry[i-1] not in (a1, a2):
				found.append(carry[i-1])
			elif xor1[i] not in (a1, a2):
				found.append(xor1[i])
		and2.append(k)
		break
	else:
		raise Exception("not found")

	# find carry
	for k, (op, a1, a2) in connections.items():
		if op is or_ and (and1[i] in (a1, a2) or and2[i] in (a1, a2)):
			if and1[i] not in (a1, a2):
				found.append(and1[i])
			elif and2[i] not in (a1, a2):
				found.append(and2[i])
			carry.append(k)
			break
	else:
		raise Exception("not found")

result = ','.join(sorted(set(found)))

print(result)
