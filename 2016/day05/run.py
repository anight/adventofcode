#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().rstrip('\n')
		return line

# Part One

door_id = load_data('input.txt')

from hashlib import md5

index = 0
result = ''

for _ in range(8):
	while not (hash := md5((door_id + str(index)).encode('ascii')).hexdigest()).startswith('00000'):
		index += 1
	index += 1
	result += hash[5]

print(result)

# Part Two

index = 0
result = list('_' * 8)

while '_' in result:
	while not (hash := md5((door_id + str(index)).encode('ascii')).hexdigest()).startswith('00000'):
		index += 1
	index += 1
	i = int(hash[5], 16)
	if i >= len(result) or result[i] != '_':
		continue
	result[i] = hash[6]

print(''.join(result))
