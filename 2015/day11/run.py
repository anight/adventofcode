#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

password = next(load_data('input.txt'))

# Part One

def next_valid_after(password):
	def next_after(password, i=-1):
		a = chr(ord(password[i]) + 1)
		carry = False
		if a in 'iol':
			a = chr(ord(a) + 1)
		elif a == chr(ord('z') + 1):
			a = 'a'
			carry = True
		password = password[:i] + a + password[len(password)+i+1:len(password)]
		if carry:
			return next_after(password, i-1)
		return password
	def valid(password):
		if 'i' in password or 'o' in password or 'l' in password:
			return False
		pairs = []
		straight3 = False
		for i in range(1, len(password)):
			if password[i] == password[i-1] and len(pairs) < 2:
				if not pairs:
					pairs.append(i-1)
				elif password[pairs[0]] != password[i]:
					pairs.append(i-1)
			elif ord(password[i]) == ord(password[i-1]) + 1:
				if i > 1 and ord(password[i-1]) == ord(password[i-2]) + 1:
					straight3 = True
		return len(pairs) == 2 and straight3
	while password != 'z' * len(password):
		password = next_after(password)
		if valid(password):
			return password
	raise Exception("Not found")

result = next_valid_after(password)

print(result)

# Part Two

result = next_valid_after(result)

print(result)

