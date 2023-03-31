#! /usr/bin/env python3

target = { 'y_from': -148, 'y_to': -89, 'x_from': 139, 'x_to': 187 }

# Part One

def launch(vx, vy):
	x, y = 0, 0
	highest_y = 0
	while True:
		x += vx
		y += vy
		if highest_y < y:
			highest_y = y
		if target['x_from'] <= x <= target['x_to'] and target['y_from'] <= y <= target['y_to']:
			return True, highest_y
		if y < target['y_from']:
			return False, highest_y
		if vx > 0:
			vx -= 1
		vy -= 1

record_y = None

for vx in range(1, 200):
	for vy in range(-200, 200):
		hit, highest_y = launch(vx, vy)
		if not hit:
			continue
		if record_y is None:
			record_y = highest_y
		else:
			if record_y < highest_y:
				record_y = highest_y

print(record_y)

# Part Two

num = 0

for vx in range(1, 200):
	for vy in range(-200, 200):
		hit, _ = launch(vx, vy)
		if hit:
			num += 1

print(num)
