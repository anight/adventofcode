#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		n = None
		for line in f:
			line = line.rstrip()
			n = Num(int(line), n)
			yield n

class Num:
	def __init__(self, n, prev):
		self.n = n
		self.next = None
		if prev is not None:
			prev.next = self

	def __repr__(self):
		return str(self.n)

def cycle(n):
	zero = None
	while n is not None:
		if zero is None and n.n == 0:
			zero = n
		i = nums.index(n)
		nums.pop(i)
		i += n.n
		if i < 0:
			i = len(nums) - (abs(i) % len(nums))
		nums.insert(i % len(nums), n)
		n = n.next
	i = nums.index(zero)
	return sum( nums[j % len(nums)].n for j in range(i + 1000, 4000, 1000) )

# Part One

nums = list(load_data('input.txt'))

result = cycle(nums[0])
print(result)

# Part Two

magic_prime_number = 811589153

nums = list(load_data('input.txt'))
for n in nums:
	n.n *= magic_prime_number

head = nums[0]
for _ in range(10):
	result = cycle(head)

print(result)

