#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' -> ')
			if t[0][0] in '%&':
				type = t[0][0]
				t[0] = t[0][1:]
			else:
				type = None
			yield t[0], type, t[1].split(', ')

# Part One

from collections import defaultdict

class Circuit:

	def __init__(self, load_data):
		self.inputs = defaultdict(lambda: list())

		self.modules = {}
		for name, t, lst in load_data:
			self.modules[name] = (t, lst)
			for l in lst:
				self.inputs[l].append(name)

		self.init_states()

		self.current_signals = []
		self.total_low = 0
		self.total_high = 0

	def init_states(self):
		self.states = {}
		for name, (t, _) in self.modules.items():
			if t == '%':
				self.states[name] = 0
			else:
				self.states[name] = {}
				for inp in self.inputs[name]:
					self.states[name][inp] = 0

	def send_signal(self, m_f, signal, lst):
		for out in lst:
			self.current_signals.append( (m_f, signal, out) )
			if signal:
				self.total_high += 1
			else:
				self.total_low += 1

	def run(self, conjunctions_of_interest=None):
		ret = None
		self.current_signals[:] = [ (None, 0, 'button') ]

		while len(self.current_signals) > 0:
			m_f, signal, m_t = self.current_signals.pop(0)
			match m_t:
				case 'button':
					self.send_signal(m_t, signal, ['broadcaster'])
				case 'broadcaster':
					_, lst = self.modules[m_t]
					self.send_signal(m_t, signal, lst)
				case _:

					if m_t not in self.modules:
						assert m_t == "rx"
						continue

					t, lst = self.modules[m_t]
					match t:
						case '%':
							state = self.states[m_t]
							if signal == 0:
								state = 1 - state
								self.states[m_t] = state
								self.send_signal(m_t, state, lst)
						case '&':
							state = self.states[m_t]
							state[m_f] = signal
							pulse = 1 - all(state.values())
							if conjunctions_of_interest is not None and \
								m_t in conjunctions_of_interest and \
								pulse == 1:
								ret = m_t
							self.send_signal(m_t, pulse, lst)
		return ret

c = Circuit(load_data('input.txt'))

for _ in range(1000):
	c.run()

print(c.total_low * c.total_high)

# Part Two

c = Circuit(load_data('input.txt'))

final_conjunction = c.inputs['rx'][0]
conjunctions_of_interest = c.inputs[final_conjunction]

presses = 0
periods = []

while len(periods) < 4:
	presses += 1
	module = c.run(conjunctions_of_interest)
	if module is not None:
		periods.append(presses)

import math

print(math.lcm(*periods))
