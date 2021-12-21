#! /usr/bin/env python3

def find_loop_size(key):
	i = 1
	loop_size = 0
	while True:
		i *= 7
		i %= 20201227
		loop_size += 1
		if i == key:
			return loop_size

def transform(subject_num, loop_size):
	i = 1
	for _ in range(loop_size):
		i *= subject_num
		i %= 20201227
	return i

# A test
card_pub_key = 5764801
door_pub_key = 17807724

card_loop_size = find_loop_size(card_pub_key)
door_loop_size = find_loop_size(door_pub_key)

assert 8 == card_loop_size
assert 11 == door_loop_size

assert 14897079 == transform(door_pub_key, card_loop_size)
assert 14897079 == transform(card_pub_key, door_loop_size)

# Part One
card_pub_key = 12320657
door_pub_key = 9659666

card_loop_size = find_loop_size(card_pub_key)
door_loop_size = find_loop_size(door_pub_key)

print(transform(door_pub_key, card_loop_size))
