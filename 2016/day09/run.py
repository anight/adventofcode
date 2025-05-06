#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		return f.readline().rstrip('\n')

# Part One

text = load_data('input.txt')

def decompress(text):
	ret = ''
	while '(' in text:
		opening_bracket = text.index('(')
		ret += text[:opening_bracket]
		text = text[opening_bracket:]
		closing_bracket = text.index(')')
		marker = text[1:closing_bracket]
		text = text[closing_bracket+1:]
		t = marker.split('x')
		num = int(t[0])
		cnt = int(t[1])
		for _ in range(cnt):
			ret += text[:num]
		text = text[num:]
	ret += text
	return ret

print(len(decompress(text)))

# Part Two

def decompressed_len(text, m=1):
	ret = 0
	while '(' in text:
		opening_bracket = text.index('(')
		ret += m * opening_bracket
		text = text[opening_bracket:]
		closing_bracket = text.index(')')
		marker = text[1:closing_bracket]
		text = text[closing_bracket+1:]
		t = marker.split('x')
		num = int(t[0])
		cnt = int(t[1])
		ret += m * decompressed_len(text[:num], cnt)
		text = text[num:]
	ret += m * len(text)
	return ret

print(decompressed_len(text))

