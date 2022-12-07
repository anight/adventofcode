#! /usr/bin/env python3

from dataclasses import dataclass, field
from functools import cached_property

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			t = line.split(' ')
			if line.startswith('$'):
				yield Command(cmd=t[1], args=t[2:])
			elif t[0][0].isnumeric():
				yield File(name=t[1], size=int(t[0]))
			elif t[0] == "dir":
				yield Dir(name=t[1])

@dataclass
class Command:
	cmd: str
	args: list[str]

@dataclass
class Dir:
	name: str
	contents: dict = field(default_factory=dict)

	def root(self):
		dir = self
		while dir.name != '/':
			dir = dir.parent
		return dir

	def subdirs(self):
		yield self
		for item in self.contents.values():
			if type(item) is Dir:
				yield from item.subdirs()

	@cached_property
	def size(self):
		size = 0
		for item in self.contents.values():
			match item:
				case File() as file:
					size += file.size
				case Dir() as dir:
					size += dir.size
		return size

@dataclass
class File:
	name: str
	size: int

def parse_fs(load_data):
	current_dir = None

	for item in load_data:
		match item:
			case Command() as c:
				if c.cmd == "cd":
					if c.args[0] == "..":
						current_dir = current_dir.parent
					else:
						if current_dir is None:
							current_dir = Dir(c.args[0])
						else:
							current_dir = current_dir.contents[c.args[0]]
				elif c.cmd == "ls":
					current_dir.contents = {}
			case File() as file:
				current_dir.contents[file.name] = file
			case Dir() as dir:
				dir.parent = current_dir
				current_dir.contents[dir.name] = dir

	return current_dir.root()

root = parse_fs(load_data('input.txt'))

# Part One

total = 0
for dir in root.subdirs():
	size = dir.size
	if size <= 100_000:
		total += size

print(total)

# Part Two

total = 70_000_000
needed = 30_000_000
free = total - root.size
to_delete = needed - free

best_candidate = None
for dir in root.subdirs():
	size = dir.size
	if size >= to_delete:
		if best_candidate is None or best_candidate.size > size:
			best_candidate = dir

print(best_candidate.size)
