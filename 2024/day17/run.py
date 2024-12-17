#! /usr/bin/env python3

def load_data(filename):
	regs = {}
	programm = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			if line == '':
				continue
			t = line.split(': ')
			if t[0].startswith('Register'):
				regs[t[0][-1]] = int(t[1])
			elif t[0] == 'Program':
				program = list(map(int, t[1].split(',')))
	return regs, program

# Part One

class InvalidOperand(Exception): pass

class VM:
	def __init__(self, program):
		self.program = program
		self.reset()

	def reset(self):
		self.pc = 0
		self.regs = {'A': 0, 'B': 0, 'C': 0}
		self.output = []

	def set_regs(self, regs):
		self.regs.update(regs)

	def run(self):
		while self.pc < len(self.program):
			self.op()
		return self.output

	def op(self):
		opcodes = ('adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv')
		opcode = opcodes[self.program[self.pc]]
		operand = self.program[self.pc+1]
#		print(opcode, operand)
		getattr(self, f'op_{opcode}')(operand)

	def combo(self, arg):
		if 0 <= arg <= 3:
#			print('  imm', arg)
			return arg
		if 4 <= arg <= 6:
			reg = chr(ord('A') + arg-4)
#			print(f'  {reg} = {self.regs[reg]}')
			return self.regs[reg]
		raise InvalidOperand(arg)

	def op_adv(self, arg):
		value = self.combo(arg)
#		self.regs['A'] //= 2 ** value
		self.regs['A'] >>= value
#		print(f"  A <- {self.regs['A']}")
		self.pc += 2

	def op_bxl(self, arg):
		self.regs['B'] ^= arg
#		print(f"  B <- {self.regs['B']}")
		self.pc += 2

	def op_bst(self, arg):
		value = self.combo(arg)
		self.regs['B'] = value & 0b111
#		print(f"  B <- {self.regs['B']}")
		self.pc += 2

	def op_jnz(self, arg):
		if self.regs['A'] != 0:
			self.pc = arg
		else:
			self.pc += 2

	def op_bxc(self, arg):
		self.regs['B'] ^= self.regs['C']
#		print(f"  B <- {self.regs['B']}")
		self.pc += 2

	def op_out(self, arg):
		value = self.combo(arg) & 0b111
		self.output.append(value)
		self.pc += 2

	def op_bdv(self, arg):
		value = self.combo(arg)
#		self.regs['B'] = self.regs['A'] // 2 ** value
		self.regs['B'] = self.regs['A'] >> value
#		print(f"  B <- {self.regs['B']}")
		self.pc += 2

	def op_cdv(self, arg):
		value = self.combo(arg)
#		self.regs['C'] = self.regs['A'] // 2 ** value
		self.regs['C'] = self.regs['A'] >> value
#		print(f"  C <- {self.regs['C']}")
		self.pc += 2


regs, program = load_data('input.txt')

vm = VM(program)
vm.set_regs(regs)
result = vm.run()

print(','.join(map(str, result)))


# Part Two

def run(regA):
	vm.reset()
	vm.set_regs({'A': regA})
	return vm.run()

results = []

def find_digit(i=0, regA=0):
	if i == len(program):
		results.append(regA)
		return
	for v in range(8):
		testA = (regA << 3) + v
		output = run(testA)
		if output[-i-1] == program[-i-1]:
			find_digit(i+1, testA)

find_digit()

print(min(results))
