#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for c in f.readline().rstrip():
			yield c

from itertools import cycle
import numpy as np

# Part One

class Tetris:
	figures = [
		['####'],

		['.#.',
		 '###',
		 '.#.',],

		['..#',
		 '..#',
		 '###',],

		['#',
		 '#',
		 '#',
		 '#',],

		['##',
		 '##',],
	]

	def __init__(self, commands):
		self.compile_figures()
		self.commands = cycle(commands)
		self.field = np.array([ [1] * 9 ], dtype=int)
		self.next_figure = 0
		self.used_commands = 0
		self.total_figures = 0
		self.total_usage = 0

	def compile_figures(self):
		def compile_figure(figure):
			return np.array([ list(map(int, line.replace('#', '1').replace('.', '0'))) for line in figure ], dtype=int)
		self.figures = [ compile_figure(figure) for figure in self.figures ]

	def get_next_figure(self):
		figure = self.figures[self.next_figure]
		self.next_figure += 1
		if self.next_figure == len(self.figures):
			self.next_figure = 0
		return figure

	def get_next_command(self):
		self.used_commands += 1
		return next(self.commands)

	def drop_figure(self):
		figure = self.get_next_figure()

		add_lines = figure.shape[0] + 3
		self.field = np.pad(self.field, ((add_lines, 0), (0, 0)))
		self.field[:add_lines,0] = 1
		self.field[:add_lines,8] = 1

		x, y = 3, 0
		fy, fx = np.asarray(figure == 1).nonzero()
		while True:
			cmd = self.get_next_command()
			dx = {'<': -1, '>': 1}[cmd]
			if not np.any(self.field[(fy + [y], fx + [x+dx])]):
				x += dx
			if np.any(self.field[(fy + [y+1], fx + [x])]):
				break
			y += 1

		self.field[(fy + [y], fx + [x])] = 1
		clean = 0
		while np.all(self.field[clean] == [1, 0, 0, 0, 0, 0, 0, 0, 1]):
			clean += 1
		self.field = self.field[clean:,...]

		self.total_figures += 1

	def state(self):
		ret = []
		for i in range(1, 8):
			c = 0
			while self.field[c,i] == 0:
				c += 1
			ret.append(c)
		return tuple([self.next_figure] + ret)

	def usage(self):
		return self.total_usage + self.field.shape[0] - 1

t = Tetris(load_data('input.txt'))
for _ in range(2022):
	t.drop_figure()

print(t.usage())

# Part Two

limit = 1_000_000_000_000
cmds = list(load_data('input.txt'))
t = Tetris(cmds)

history = {}
tracking = True
while t.total_figures < limit:
	t.drop_figure()
	if not tracking:
		continue
	key = t.used_commands % len(cmds)
	state = t.state()
	value = (t.usage(), t.total_figures, state)
	if key not in history:
		history[key] = [value]
	else:
		for prev_usage, prev_total_figures, prev_state in history[key]:
			if prev_state == state:
				period = t.total_figures - prev_total_figures
				n = (limit - t.total_figures) // period
				t.total_usage += (t.usage() - prev_usage) * n
				t.total_figures += period * n
				tracking = False
				break
		else:
			history[key].append(value)

print(t.usage())
