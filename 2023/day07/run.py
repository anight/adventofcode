#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			c = line.split()
			yield c[0], int(c[1])

# Part One

from dataclasses import dataclass
from collections import Counter

@dataclass
class Hand:
	cards: list
	bid: int

	FIVE = 1
	FOUR = 2
	FULL_HOUSE = 3
	THREE = 4
	TWO_PAIRS = 5
	ONE_PAIR = 6
	HIGH_CARD = 7

	hand_type = {
		(5,):   FIVE,
		(4,):   FOUR,
		(3, 2): FULL_HOUSE,
		(3,):   THREE,
		(2, 2): TWO_PAIRS,
		(2,):   ONE_PAIR,
		():     HIGH_CARD,
	}

	@staticmethod
	def card_strength(card):
		return "AKQJT98765432".index(card)

	def groups(self):
		return sorted(dict(Counter(self.cards)).items(), key=lambda v: v[1], reverse=True)

	def type(self):
		t = tuple( v for _, v in self.groups() if v > 1 )
		return self.hand_type[t]

	def strength(self):
		return ( self.type(), *[ self.card_strength(c) for c in self.cards] )

	def __lt__(self, other):
		return self.strength() < other.strength()

hands = [ Hand(cards, bid) for cards, bid in load_data('input.txt') ]

print(sum( n * h.bid for n, h in enumerate(sorted(hands, reverse=True), start=1)))

# Part Two

class HandWithJforJoker(Hand):

	@staticmethod
	def card_strength(card):
		return "AKQT98765432J".index(card)

	def type(self):
		jokers = Counter(self.cards).get('J', 0)
		t = tuple( v for k, v in self.groups() if k != 'J' and v > 1 )
		base_type = self.hand_type[t]
		return {
			Hand.HIGH_CARD:    [Hand.HIGH_CARD, Hand.ONE_PAIR, Hand.THREE, Hand.FOUR, Hand.FIVE, Hand.FIVE],
			Hand.ONE_PAIR:     [Hand.ONE_PAIR, Hand.THREE, Hand.FOUR, Hand.FIVE],
			Hand.TWO_PAIRS:    [Hand.TWO_PAIRS, Hand.FULL_HOUSE],
			Hand.THREE:        [Hand.THREE, Hand.FOUR, Hand.FIVE],
			Hand.FULL_HOUSE:   [Hand.FULL_HOUSE],
			Hand.FOUR:         [Hand.FOUR, Hand.FIVE],
			Hand.FIVE:         [Hand.FIVE],
		}[base_type][jokers]

hands = [ HandWithJforJoker(cards, bid) for cards, bid in load_data('input.txt') ]

print(sum( n * h.bid for n, h in enumerate(sorted(hands, reverse=True), start=1)))
