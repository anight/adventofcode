#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		a = []
		for line in f:
			line = line.rstrip()
			a.append(list(map(int, line)))
		return np.array(a, dtype=int)

import numpy as np

# Part One

trees = load_data('input.txt')

def mark_visible(trees, visible):

	def mark_visible_from_top():
		for x in range(0, trees.shape[1]):
			highest = -1
			for y in range(0, trees.shape[0]):
				if trees[y,x] > highest:
					visible[y,x] = 1
					highest = trees[y,x]
					if highest == 9: break

	for _ in range(4):
		mark_visible_from_top()
		trees = np.rot90(trees)
		visible = np.rot90(visible)

visible = np.zeros_like(trees)
mark_visible(trees, visible)

print(np.sum(visible))

# Part Two

def count_visible(x, y):
	this = trees[y,x]

	def count_one_side(rx, ry):
		cnt = 0
		for ty in ry:
			for tx in rx:
				cnt += 1
				if trees[ty,tx] >= this:
					return cnt
		return cnt

	return count_one_side(range(x, x+1), range(y+1, trees.shape[0]))   * \
	       count_one_side(range(x, x+1), range(y-1, -1, -1))           * \
	       count_one_side(range(x+1, trees.shape[1]), range(y, y+1))   * \
	       count_one_side(range(x-1, -1, -1), range(y, y+1))

best = 0
for y in range(1, trees.shape[0]-1):
	for x in range(1, trees.shape[1]-1):
		score = count_visible(x, y)
		if best < score:
			best = score

print(best)
