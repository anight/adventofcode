#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		line = f.readline().strip()
		return line

# Part One

message = load_data('input.txt')

class Packet(object):
	def __init__(self, binary=None, hex=None):
		if hex is not None:
			self.body = ''.join( self.decode_hex(c) for c in hex )
		else:
			self.body = binary
		self.version = None
		self.type_id = None
		self.subpackets = []
		self.parse()

	def decode_hex(self, h):
		return '{:04b}'.format(int(h, base=16))

	def parsenum(self, bits):
		assert len(self.body) >= self.i+bits
		ret = int(self.body[self.i:self.i+bits], base=2)
		self.i += bits
		return ret

	def parse(self):
		self.i = 0
		self.version = self.parsenum(3)
		self.type_id = self.parsenum(3)
		if self.type_id == 4: # "literal value"
			self.literal_value = 0
			while True:
				keep_reading = self.parsenum(1)
				bits = self.parsenum(4)
				self.literal_value *= 16
				self.literal_value += bits
				if not keep_reading:
					break
		else: # "operator"
			length_type_id = self.parsenum(1)
			if length_type_id:
				num_of_packets = self.parsenum(11)
				for _ in range(num_of_packets):
					p = Packet(self.body[self.i:])
					self.subpackets.append(p)
					self.i += p.i
			else:
				packets_length = self.parsenum(15)
				while packets_length > 0:
					p = Packet(self.body[self.i:])
					self.subpackets.append(p)
					self.i += p.i
					packets_length -= p.i

	def value(self):
		if self.type_id == 0:
			return sum( p.value() for p in self.subpackets )
		if self.type_id == 1:
			product = 1
			for p in self.subpackets:
				product *= p.value()
			return product
		if self.type_id == 2:
			return min( p.value() for p in self.subpackets )
		if self.type_id == 3:
			return max( p.value() for p in self.subpackets )
		if self.type_id == 4:
			return self.literal_value
		if self.type_id == 5:
			return int( self.subpackets[0].value() > self.subpackets[1].value() )
		if self.type_id == 6:
			return int( self.subpackets[0].value() < self.subpackets[1].value() )
		if self.type_id == 7:
			return int( self.subpackets[0].value() == self.subpackets[1].value() )
		raise "oops"

	def get_all_versions(self):
		yield self.version
		for p in self.subpackets:
			yield from p.get_all_versions()

parsed = Packet(hex=message)

print(sum(v for v in parsed.get_all_versions()))

# Part Two

print(parsed.value())

