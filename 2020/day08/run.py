#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line.split(' ')
			yield t[0], int(t[1])

class HandheldGameConsole:
	def __init__(self, ops):
		self.ops = list(ops)
		self.reset()

	def reset(self):
		self.ip = 0
		self.acc = 0

	def exec_op(self):
		op, arg = self.ops[self.ip]
		match op:
			case 'nop':
				self.ip += 1
			case 'acc':
				self.acc += arg
				self.ip += 1
			case 'jmp':
				self.ip += arg

	def reached_end(self):
		return self.ip == len(self.ops)

	def run_until_looped(self):
		visited = {}
		self.reset()
		while self.ip not in visited and not self.reached_end():
			visited[self.ip] = None
			self.exec_op()
		return self.reached_end()

	def brute_force_flip_op(self):
		for i, (op, arg) in enumerate(self.ops):
			if op == 'nop':
				self.ops[i] = ('jmp', arg)
				if self.run_until_looped():
					return
				self.ops[i] = ('nop', arg)
			elif op == 'jmp':
				self.ops[i] = ('nop', arg)
				if self.run_until_looped():
					return
				self.ops[i] = ('jmp', arg)

# Part One

console = HandheldGameConsole(load_data('input.txt'))
console.run_until_looped()
print(console.acc)

# Part Two

console.brute_force_flip_op()
print(console.acc)
