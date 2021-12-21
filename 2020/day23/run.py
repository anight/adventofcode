#! /usr/bin/env python3

class Node:

	def __init__(self, value):
		self.value = value
		self.prev = self
		self.next = self

	def insert_before(self, prev):
		prev.next = self
		prev.prev = self.prev
		self.prev.next = prev
		self.prev = prev

	def insert_after(self, next):
		next.prev = self
		next.next = self.next
		self.next.prev = next
		self.next = next

	def unlink(self):
		self.next.prev = self.prev
		self.prev.next = self.next
		self.next = self
		self.prev = self
		return self

class Cups:

	def __init__(self, numbers):
		self.min = int(1e9)
		self.max = int(-1e9)
		self.current = None
		self.by_value = {}
		for num in numbers:
			num = int(num)
			node = Node(num)
			if self.current is None:
				self.current = node
			else:
				self.current.insert_before(node)
			self.by_value[num] = node
			if num < self.min:
				self.min = num
			if num > self.max:
				self.max = num

	def ordered_from_one(self):
		node = self.by_value[1].next
		ret = ''
		while node.value != 1:
			ret += str(node.value)
			node = node.next
		return ret

	def move(self):
		picked = self.current.next.unlink()
		picked.insert_before(self.current.next.unlink())
		picked.insert_before(self.current.next.unlink())
		dest = self.current.value - 1
		if dest < self.min:
			dest = self.max
		while dest == picked.value or dest == picked.next.value or dest == picked.prev.value:
			dest -= 1
			if dest < self.min:
				dest = self.max
		dest = self.by_value[dest]
		dest.insert_after(picked.prev.unlink())
		dest.insert_after(picked.prev.unlink())
		dest.insert_after(picked.prev.unlink())
		self.current = self.current.next

# A test

cups = Cups("389125467")

for _ in range(10):
	cups.move()

assert cups.ordered_from_one() == "92658374"

for _ in range(90):
	cups.move()

assert cups.ordered_from_one() == "67384529"

# Part One

cups = Cups("538914762")

for _ in range(100):
	cups.move()

print(cups.ordered_from_one())

# Part Two

print("initializing...")

cups = Cups(list(map(int, "538914762")) + list(range(10, 1000001)))

print("calculating, please wait about 70 sec...")

for _ in range(10000000):
	cups.move()

print(cups.by_value[1].next.value * cups.by_value[1].next.next.value)

