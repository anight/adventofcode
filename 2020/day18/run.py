#! /usr/bin/env python3

def all_samples(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.rstrip()

from ply import lex, yacc

class Lexer:
	tokens = (
		'NUMBER',
		'PLUS',
		'TIMES',
		'LPAREN',
		'RPAREN',
	)

	t_PLUS    = r'\+'
	t_TIMES   = r'\*'
	t_LPAREN  = r'\('
	t_RPAREN  = r'\)'

	t_ignore  = ' '

	def t_NUMBER(self, t):
		r'\d+'
		t.value = int(t.value)
		return t

	def t_error(self, t):
		print("Unexpected character '%s'" % t.value[0])
		t.lexer.skip(1)

	def __init__(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

class Parser(Lexer):

	def p_error(self, p):
		print("Syntax error in input!")

	def __init__(self, **kwargs):
		super(Parser, self).__init__(**kwargs)
		self.parser = yacc.yacc(module=self, debug=0, write_tables=0, **kwargs)

	def parse(self, text):
		return self.parser.parse(text, lexer=self.lexer)

# Part One

class ParserPartOne(Parser):

	def p_expression(self, p):
		'''expression : term'''
		p[0] = p[1]

	def p_term_num(self, p):
		'''term : NUMBER'''
		p[0] = p[1]

	def p_expression_binop(self, p):
		'''expression : expression PLUS term
		 | expression TIMES term'''
		if p[2] == '+':
			p[0] = p[1] + p[3]
		elif p[2] == '*':
			p[0] = p[1] * p[3]

	def p_term_expr(self, p):
		'''term : LPAREN expression RPAREN'''
		p[0] = p[2]

total = 0

for line in all_samples('input.txt'):
	total += ParserPartOne().parse(line)

print(total)

# Part Two

class ParserPartTwo(Parser):

	def p_expression2(self, p):
		'''expression : term'''
		p[0] = p[1]

	def p_expression_times(self, p):
		'''expression : expression TIMES term'''
		p[0] = p[1] * p[3]

	def p_term_plus(self, p):
		'''term : term PLUS factor'''
		p[0] = p[1] + p[3]

	def p_term_factor(self, p):
		'''term : factor'''
		p[0] = p[1]

	def p_factor_num(self, p):
		'''factor : NUMBER'''
		p[0] = p[1]

	def p_factor_exp(self, p):
		'''factor : LPAREN expression RPAREN'''
		p[0] = p[2]

total = 0

for line in all_samples('input.txt'):
	total += ParserPartTwo().parse(line)

print(total)

