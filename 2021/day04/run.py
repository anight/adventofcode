#! /usr/bin/env python3

import numpy as np

def load_data(filename):
	with open(filename, 'r') as f:
		numbers = list(map(int, f.readline().strip().split(',')))
		boards = []
		board = []
		for line in f:
			line = line.strip()
			if line == '':
				continue
			line = list(map(int, line.split()))
			board.append(line)
			if len(board) == 5:
				boards.append(board)
				board = []
	return numbers, np.array(boards, dtype=int)

# Part One

numbers, boards = load_data('input.txt')

marked = np.zeros(boards.shape, dtype=int)

for number in numbers:
	marked[np.where(boards == number)] = 1
	won_boards = set(np.where(5 == np.sum(marked, axis=2))[0]) | set(np.where(5 == np.sum(marked, axis=1))[0])
	if len(won_boards) > 0:
		break

board_no = list(won_boards)[0]
sum_of_unmarked = np.sum(boards[board_no][np.where(marked[board_no] == 0)])
print(number * sum_of_unmarked)

# Part Two

marked = np.zeros(boards.shape, dtype=int)

for number in numbers:
	won_boards = set(np.where(5 == np.sum(marked, axis=2))[0]) | set(np.where(5 == np.sum(marked, axis=1))[0])
	marked[np.where(boards == number)] = 1
	new_won_boards = set(np.where(5 == np.sum(marked, axis=2))[0]) | set(np.where(5 == np.sum(marked, axis=1))[0])
	if len(new_won_boards) == len(boards) and len(new_won_boards) > len(won_boards):
		break

board_no = list(new_won_boards - won_boards)[0]
sum_of_unmarked = np.sum(boards[board_no][np.where(marked[board_no] == 0)])
print(number * sum_of_unmarked)
