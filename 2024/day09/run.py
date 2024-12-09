#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			yield line

data = next(load_data('input.txt'))

# Part One

class Empty: pass

class Fs:
	def __init__(self, data):
		self.fs = []
		for i, ch in enumerate(data):
			if i % 2 == 0:
				self.fs += [i // 2] * int(ch)
			else:
				self.fs += [Empty] * int(ch)

	def compact(self):
		file_iter = self.each_file()
		hole_iter = self.each_hole()
		next(hole_iter)
		while True:
			file_start, file_stop = next(file_iter)
			try:
				space_start, space_stop = hole_iter.send((file_start, file_stop))
			except StopIteration:
				break
			if space_start is None:
				continue
			# swap file and empty space
			self.fs[file_start:file_stop], self.fs[space_start:space_stop] = \
				self.fs[space_start:space_stop], self.fs[file_start:file_stop]

	def checksum(self):
		return sum( i * n for i, n in enumerate(self.fs) if n is not Empty )

class Part1(Fs):

	def each_file(self):
		for i in range(len(self.fs)-1, 0, -1):
			if self.fs[i] is not Empty:
				yield i, i+1

	def each_hole(self):
		file_start, file_stop = yield None
		for i in range(len(self.fs)):
			if i >= file_start:
				break
			if self.fs[i] is Empty:
				file_start, file_stop = yield i, i+1
fs = Part1(data)
fs.compact()
print(fs.checksum())

# Part Two

class Part2(Fs):

	@staticmethod
	def groups(iterator):
		start = 0
		try:
			prev = next(iterator)
		except StopIteration:
			return
		cnt = 1
		for current in iterator:
			if current == prev:
				cnt += 1
			else:
				yield start, cnt, prev
				prev = current
				start += cnt
				cnt = 1
		yield start, cnt, prev

	def each_file(self):
		processed = set()
		for start, cnt, item in self.groups(reversed(self.fs)):
			if item is Empty or item in processed:
				continue
			start = len(self.fs) - start - cnt
			yield start, start + cnt
			processed.add(item)

	def all_holes_by_size(self):
		holes = {}
		for start, cnt, item in self.groups(iter(self.fs)):
			if item is not Empty:
				continue
			if cnt not in holes:
				holes[cnt] = [start]
			else:
				holes[cnt].append(start)
		return holes

	def each_hole(self):
		holes = self.all_holes_by_size()
		keys = sorted(holes.keys())
		file_start, file_stop = yield None
		while True:
			file_len = file_stop - file_start
			at_least_one_hole = False
			hole_start = len(self.fs)
			hole_size = 0
			for size in keys:
				if len(holes[size]) == 0:
					continue
				start = holes[size][0]
				if start >= file_start:
					continue
				at_least_one_hole = True
				if file_len > size:
					continue
				if start < hole_start:
					hole_start = start
					hole_size = size
			if hole_size:
				file_start, file_stop = yield hole_start, hole_start + file_len
				holes[hole_size] = holes[hole_size][1:]
				rest_size = hole_size - file_len
				rest_start = hole_start + file_len
				if rest_size > 0:
					for i in range(len(holes[rest_size])):
						if holes[rest_size][i] > rest_start:
							break
					holes[rest_size].insert(i, rest_start)
			else:
				if not at_least_one_hole:
					break
				file_start, file_stop = yield None, None

fs = Part2(data)
fs.compact()
print(fs.checksum())
