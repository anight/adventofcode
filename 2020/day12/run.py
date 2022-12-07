#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			yield line[0], int(line[1:])

# Part One

class Ship:
	def __init__(self, load_data):
		self.e = 0
		self.n = 0
		self.direction = 'E'
		self.load_data = load_data

	def navigate(self):
		for action, value in self.load_data:
			getattr(self, action)(value)

	def N(self, value):
		self.n += value

	def S(self, value):
		self.n -= value

	def E(self, value):
		self.e += value

	def W(self, value):
		self.e -= value

	def L(self, value):
		self.direction = "ENWS"[("ENWS".index(self.direction) + value // 90) % 4]

	def R(self, value):
		self.L(360-value)

	def F(self, value):
		getattr(self, self.direction)(value)

ship = Ship(load_data('input.txt'))
ship.navigate()
print(abs(ship.e) + abs(ship.n))

# Part Two

class Ship2(Ship):
	def __init__(self, load_data):
		super(Ship2, self).__init__(load_data)
		self.wp_e = 10
		self.wp_n = 1

	def N(self, value):
		self.wp_n += value

	def S(self, value):
		self.wp_n -= value

	def E(self, value):
		self.wp_e += value

	def W(self, value):
		self.wp_e -= value

	def L(self, value):
		if value == 90:
			self.wp_e, self.wp_n = -self.wp_n, self.wp_e
		elif value == 180:
			self.wp_e, self.wp_n = -self.wp_e, -self.wp_n
		elif value == 270:
			self.wp_e, self.wp_n = self.wp_n, -self.wp_e

	def F(self, value):
		self.e += value * self.wp_e
		self.n += value * self.wp_n

ship = Ship2(load_data('input.txt'))
ship.navigate()
print(abs(ship.e) + abs(ship.n))
