#! /usr/bin/env python3

class State:
	def __init__(self, rooms, hallway, energy):
		self.rooms = rooms
		self.hallway = hallway
		self.energy = energy

	def key(self):
		return tuple(self.rooms + self.hallway)

	def __repr__(self):
		hallway_str = ''.join([ '.' if c is None else c for c in self.hallway ])
		return '[<{}> <{}> <{}> <{}>] [{}] ({})'.format(self.rooms[0], self.rooms[1], self.rooms[2], self.rooms[3], hallway_str, self.energy)

	def possible_moves(self):
		# try all possible moves "from hallway to room"
		for i, amphipod in enumerate(self.hallway):
			if amphipod is None:
				continue
			target_room_no = 'ABCD'.index(amphipod)
			price_per_move = [1, 10, 100, 1000][target_room_no]
			if self.rooms[target_room_no] != amphipod * len(self.rooms[target_room_no]):
				continue
			# room is ready for this one
			moves = self.moves_from_hallway_to_room(i, target_room_no)
			if moves is None:
				continue
			# path is free
			new_hallway = list(self.hallway)
			new_hallway[i] = None
			new_rooms = list(self.rooms)
			new_rooms[target_room_no] = amphipod + new_rooms[target_room_no]
			energy = moves * price_per_move
			yield State(new_rooms, new_hallway, energy)

		# try all possible "room to room" moves
		for room_no, roommates in enumerate(self.rooms):
			if len(roommates) == 0:
				continue
			amphipod = roommates[0]
			target_room_no = 'ABCD'.index(amphipod)
			price_per_move = [1, 10, 100, 1000][target_room_no]
			if room_no == target_room_no:
				continue
			if self.rooms[target_room_no] != amphipod * len(self.rooms[target_room_no]):
				continue
			moves = self.moves_from_room_to_room(room_no, target_room_no)
			if moves is None:
				continue
			# path is free
			new_rooms = list(self.rooms)
			new_rooms[room_no] = new_rooms[room_no][1:]
			new_rooms[target_room_no] = amphipod + new_rooms[target_room_no]
			energy = moves * price_per_move
			yield State(new_rooms, list(self.hallway), energy)

		# try all possible "from room to hallway" moves
		for room_no, roommates in enumerate(self.rooms):
			if len(roommates) == 0:
				continue
			amphipod = roommates[0]
			target_room_no = 'ABCD'.index(amphipod)
			price_per_move = [1, 10, 100, 1000][target_room_no]
			if len(self.rooms[room_no]) > 0 and self.rooms[room_no] == 'ABCD'[room_no] * len(self.rooms[room_no]):
				continue
			for hallway_position in range(len(self.hallway)):
				if hallway_position in (2, 4, 6, 8):
					continue
				moves = self.moves_from_room_to_hallway(room_no, hallway_position)
				if moves is None:
					continue
				new_rooms = list(self.rooms)
				new_rooms[room_no] = new_rooms[room_no][1:]
				new_hallway = list(self.hallway)
				new_hallway[hallway_position] = amphipod
				energy = moves * price_per_move
				yield State(new_rooms, new_hallway, energy)

	def moves_from_hallway_to_room(self, hallway_position, target_room_no):
		target_room_position = 2 + 2 * target_room_no
		if target_room_position > hallway_position:
			d = 1
		else:
			d = -1
		moves = 0
		while hallway_position != target_room_position:
			hallway_position += d
			if self.hallway[hallway_position] is not None:
				return None
			moves += 1
		return moves + ROOM_CAPACITY - len(self.rooms[target_room_no])

	def moves_from_room_to_room(self, room_no, target_room_no):
		moves = 1 + ROOM_CAPACITY - len(self.rooms[room_no])
		room_position = 2 + 2 * room_no
		target_room_position = 2 + 2 * target_room_no
		f, t = min(room_position, target_room_position), max(room_position, target_room_position)
		if self.hallway[f:t+1] != [None]*(t-f+1):
			return None
		moves += t - f
		return moves + ROOM_CAPACITY - len(self.rooms[target_room_no])

	def moves_from_room_to_hallway(self, room_no, hallway_position):
		moves = 1 + ROOM_CAPACITY - len(self.rooms[room_no])
		room_position = 2 + 2 * room_no
		f, t = min(room_position, hallway_position), max(room_position, hallway_position)
		if self.hallway[f:t+1] != [None]*(t-f+1):
			return None
		return moves + (t - f)

from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	item: Any=field(compare=False)
	def __init__(self, priority, state):
		self.priority = priority
		self.item = state

class Game:
	def __init__(self):
		self.states = {}

	def dijkstra(self, state):
		D = {}
		D[state.key()] = 0
		pq = PriorityQueue()
		pq.put(PrioritizedItem(0, state))
		while not pq.empty():
			pi = pq.get()
			state = pi.item
			self.states[state.key()] = state

			for new_state in state.possible_moves():
				if new_state.key() not in self.states:
					old_cost = D.get(new_state.key(), float('inf'))
					new_cost = D[state.key()] + new_state.energy
					if new_cost < old_cost:
						pq.put(PrioritizedItem(new_cost, new_state))
						D[new_state.key()] = new_cost
		return D

# Part One

initial_state = State(['CB', 'AA', 'DB', 'DC'], [None]*11, 0)
final_state = State(['AA', 'BB', 'CC', 'DD'], [None]*11, 0)

ROOM_CAPACITY = 2

D = Game().dijkstra(initial_state)

print(D[final_state.key()])

# Part Two

initial_state = State(['CDDB', 'ACBA', 'DBAB', 'DACC'], [None]*11, 0)
final_state = State(['AAAA', 'BBBB', 'CCCC', 'DDDD'], [None]*11, 0)

ROOM_CAPACITY = 4

D = Game().dijkstra(initial_state)

print(D[final_state.key()])
