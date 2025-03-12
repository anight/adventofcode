#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

# Part One

def dequoted_unescaped(string):
	ret = ''
	string = string[1:-1]
	escaped = None
	for i, ch in enumerate(string):
		if escaped is not None:
			if string[escaped+1] == 'x':
				if i == escaped + 3:
					ret += chr(int(string[escaped+2:escaped+4], 16))
					escaped = None
			else:
				ret += ch
				escaped = None
		elif ch == '\\':
			escaped = i
		else:
			ret += ch
	return ret

result = sum(len(line) - len(dequoted_unescaped(line)) for line in load_data('input.txt'))

print(result)

# Part Two

def quoted_escaped(string):
	ret = ''
	for ch in string:
		if ch in ('"', '\\'):
			ret += '\\' + ch
		elif ord(ch) >= 128:
			ret += f'\\x{ord(ch):02x}'
		else:
			ret += ch
	return '"' + ret + '"'

result = sum(len(quoted_escaped(line)) - len(line) for line in load_data('input.txt'))

print(result)
