#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			yield int(line.split(': ')[1])

# Part One

class Player(object):
	def __init__(self, player_id, position):
		self.player_id = player_id
		self.position = position
		self.score = 0

class Dice(object):
	def __init__(self):
		self.next_value = 1
		self.wrap = 100
		self.rolls = 0

	def roll(self):
		ret = self.next_value
		self.next_value += 1
		if self.next_value > self.wrap:
			self.next_value -= self.wrap
		self.rolls += 1
		return ret

dice = Dice()
players = []

for player_id, position in enumerate(load_data('input.txt'), 1):
	players.append( Player(player_id, position) )

while players[0].score < 1000 and players[1].score < 1000:
	player = players.pop(0)
	advance = dice.roll() + dice.roll() + dice.roll()
	player.position = 1 + (player.position - 1 + advance) % 10
	player.score += player.position
	players.append(player)

print(players[0].score * dice.rolls)

# Part Two

class PlayerInSuperPosition(object):

	rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

	def __init__(self, player_id, won):
		self.player_id = player_id
		self.won = won
		self.by_position = [ dict() for _ in range(11) ]
		self.players_in_game = 0

	def add(self, position, score, number):
		if score >= 21:
			self.won += number * players[0].players_in_game
			return
		if score in self.by_position[position]:
			self.by_position[position][score] += number
		else:
			self.by_position[position][score] = number
		self.players_in_game += number

	def roll(self):
		new_player = PlayerInSuperPosition(self.player_id, self.won)
		for position in range(1, 11):
			for score, number in self.by_position[position].items():
				for advance, multiply in PlayerInSuperPosition.rolls.items():
					new_position = 1 + (position - 1 + advance) % 10
					new_score = score + new_position
					new_player.add(new_position, new_score, number * multiply)
		return new_player

players = []

for player_id, position in enumerate(load_data('input.txt'), 1):
	player = PlayerInSuperPosition(player_id, 0)
	player.add(position, 0, 1)
	players.append(player)

while players[0].players_in_game > 0 or players[1].players_in_game > 0:
	player = players.pop(0)
	player = player.roll()
	players.append(player)

print(max(players[0].won, players[1].won))

