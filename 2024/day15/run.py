#! /usr/bin/env python3

def load_data(filename):
	a = {}
	moves = ''
	y = 0
	parse_moves = False
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				parse_moves = True
			elif not parse_moves:
				a.update( {x+1j*y: c for x, c in enumerate(line)} )
				y += 1
			else:
				moves += line
	return a, moves

a, moves = load_data('input.txt')
directions = {'>': 1, '^': -1j, '<': -1, 'v': 1j}

# Part One

def moveit(moves):
	r = next( k for k, v in a.items() if v == '@' )

	for m in moves:
		d = directions[m]
		distance = 0
		while a[r + d * distance] not in '#.':
			distance += 1
		if a[r + d * distance] == '#':
			continue
		while distance > 0:
			a[r + d * distance] = a[r + d * (distance-1)]
			distance -= 1
		a[r] = '.'
		r += d

moveit(moves)

def score(ch):
	return sum( int(c.real + 100 * c.imag) for c, v in a.items() if v == ch )

print(score('O'))

# Part Two

a, moves = load_data('input.txt')

new_a = { c.real * 2 + 1j * c.imag: ('[' if v == 'O' else v) for c, v in a.items() }
new_a.update( { c.real * 2 + 1 + 1j * c.imag: (']' if v == 'O' else '.' if v == '@' else v) for c, v in a.items() } )

a = new_a

class Unmovable: pass
class Empty: pass

def scan_boxes(s, d):
	b = None
	deps = []
	char = a[s]
	if char == '[':
		b = s
	elif char == ']':
		b = s-1
	elif char == '#':
		return Unmovable
	elif char == '.':
		return Empty
	assert b is not None
	if d.imag:
		# Keep scaning up or down from the box
		dep1 = scan_boxes(b+d, d)
		dep2 = scan_boxes(b+1+d, d)
		if dep1 is Unmovable or dep2 is Unmovable:
			return Unmovable
		if dep1 is not Empty:
			deps.append(dep1)
		if dep2 is not Empty and dep1 != dep2:
			deps.append(dep2)
	else:
		if d.real > 0:
			# Keep scaning right from the box
			dep = scan_boxes(b+2, d)
		else:
			# Keep scanning left from the box
			dep = scan_boxes(b-1, d)
		if dep is Unmovable:
			return Unmovable
		if dep is not Empty:
			deps.append(dep)
	return b, deps

def move(boxes, d, moved):
	if boxes is Empty:
		return
	b, deps = boxes
	for dep in deps:
		move(dep, d, moved)
	if b in moved:
		return
	moved.add(b)
	assert a[b] == '[' and a[b+1] == ']'
	if d.imag:
		assert a[b+d] == '.' and a[b+d+1] == '.'
		a[b+d] = '['
		a[b+d+1] = ']'
		a[b] = '.'
		a[b+1] = '.'
	else:
		if d.real > 0:
			assert a[b+2] == '.'
			a[b] = '.'
			a[b+1] = '['
			a[b+2] = ']'
		else:
			assert a[b-1] == '.'
			a[b+1] = '.'
			a[b] = ']'
			a[b-1] = '['

def moveit(moves):
	r = next( k for k, v in a.items() if v == '@' )

	for m in moves:
		d = directions[m]
		boxes = scan_boxes(r+d, d)
		if boxes is Unmovable:
			continue
		move(boxes, d, set())
		a[r] = '.'
		r += d
		assert a[r] == '.'
		a[r] = '@'

moveit(moves)

print(score('['))
