#! /usr/bin/env python3

def load_deck():
	with open('input.txt', 'r') as f:
		deck = {}
		player_id = None
		for line in f:
			line = line.strip()
			if line.startswith('Player '):
				player_id = int(line.split(' ')[1].strip(':'))
				deck[player_id] = []
			elif len(line) > 0:
				card = int(line)
				deck[player_id].append(card)
	return deck

def PlayCombat(deck):
	while len(deck[1]) > 0 and len(deck[2]) > 0:
		c1 = deck[1].pop(0)
		c2 = deck[2].pop(0)
		if c1 > c2:
			deck[1].append(c1)
			deck[1].append(c2)
		else:
			deck[2].append(c2)
			deck[2].append(c1)

	if len(deck[1]) > 0:
		return deck[1]
	else:
		return deck[2]

def score(winner):
	x = 0
	for i, n in enumerate(reversed(winner)):
		x += (i+1) * n
	return x

deck = load_deck()
winner = PlayCombat(deck)
print(score(winner))

def PlayRecursiveCombat(deck):
	winner = None
	history = {}

	while len(deck[1]) > 0 and len(deck[2]) > 0:
		state = ( tuple(deck[1]), tuple(deck[2]) )
		if state in history:
			winner = deck[1]
			return winner, True
		history[state] = True

		c1 = deck[1].pop(0)
		c2 = deck[2].pop(0)

		if c1 <= len(deck[1]) and c2 <= len(deck[2]):
			new_deck = {1: list(deck[1][:c1]), 2: list(deck[2][:c2])}
			_, winner_is_player1 = PlayRecursiveCombat(new_deck)
		else:
			winner_is_player1 = c1 > c2

		if winner_is_player1:
			deck[1].append(c1)
			deck[1].append(c2)
		else:
			deck[2].append(c2)
			deck[2].append(c1)

	if len(deck[1]) > 0:
		return deck[1], True
	else:
		return deck[2], False

deck = load_deck()
winner, _ = PlayRecursiveCombat(deck)
print(score(winner))
