
# most of the code borrowed from https://codereview.stackexchange.com/a/190370
# with bug fixes and additions

'''
Original EBNF:

Expression = Term {("+"|"-") Term} .
Term = Factor {("*"|"/") Factor} .
Factor = number | "(" Expression ")" .

ParserPartOne EBNF:

Expression = Item {("+"|"*") Item} .
Item = number | "(" Expression ")" .

ParserPartTwo EBNF:

Expression = Term {"*" Term} .
Term = Factor {"+" Factor} .
Factor = number | "(" Expression ")" .

'''

def calculate(parser, expression):
	"""Evaluates a mathematical expression and returns the result.

	>>> calculate('3 * (1 + 6 / 3)')
	9
	"""
	return parser(Scanner(expression).scan()).parse()

def flatten(iterable):
	"""Flattens a nested iterable by one nesting layer.

	>>> flatten([[1,2], [3]])
	[1, 2, 3]
	"""
	return [x for l in iterable for x in l]

class BaseParser:
	"""A base class containing utilities useful for a Parser."""

	def __init__(self, items):
		self._items = PeekableIterator(items)

	def _take(self, predicate):
		"""
		Yields a contiguous group of items from the items being parsed for
		which the predicate returns True.

		>>> p = BaseParser([2, 4, 3])
		>>> list(p._take(lambda x: x % 2 == 0))
		[2, 4]
		"""
		while predicate(self._items.peek()):
			ret = next(self._items)
			yield ret

	def _done(self):
		"""Returns True if the underlying items have been fully consumed."""
		try:
			self._items.peek()
			return False
		except StopIteration:
			return True


class PeekableIterator:
	"""An iterator that supports 1-lookahead (peek)."""

	def __init__(self, iterable):
		self._iterator = iter(iterable)

		# NOTE: We use None here to denote that we haven't peeked yet. This
		#	   doesn't work if None can occur in the iterable (so this
		#	   doesn't generalize!), but for our purposes here it's fine!
		self._next_item = None

	def peek(self):
		"""
		Return the next item that will be returned by the iterator without
		advancing the iterator. Raises StopIteration if the iterator is done.

		>>> i = PeekableIterator([1, 2, 3])
		>>> i.peek()
		1
		>>> i.peek()
		1
		>>> next(i)
		1
		>>> next(i)
		2
		>>> i.peek()
		3
		"""
		if self._next_item is None:
			self._next_item = next(self._iterator)

		return self._next_item

	def __next__(self):
		if self._next_item is not None:
			next_item = self._next_item
			self._next_item = None
			return next_item

		return next(self._iterator)

	def __iter__(self):
		return self

class Scanner(BaseParser):
	"""Scanner scans an input string for calculator tokens and yields them.

	>>> list(Scanner('11 * (2 + 3)').scan())
	[11, '(', 2, '+', 3, ')']
	"""

	def scan(self):
		"""Yields all tokens in the input."""
		while not self._done():
			# Ignore any whitespace that may be next
			self._consume_whitespace()

			# Emit any symbol tokens that may be next
			yield from self._take(lambda char: char in '+*()')

			# Emit any number token that may be next
			yield from self._take_number()

	def _consume_whitespace(self):
		"""_take()s whitespace characters, but does not yield them."""
		# Note we need the list here to force evaluation of the generator
		list(self._take(lambda char: char.isspace()))

	def _take_number(self):
		"""Yields a single number if there is one next in the input."""

		# Gather up the digits/. forming the next number in the input
		number = ''.join(self._take(lambda c: c.isdigit()))

		# If number is empty, we didn't scan digits, so don't try to float it
		if number:
			try:
				yield int(number)
			except ValueError:
				raise BadNumberError(number)

import operator

class ParserCommon(BaseParser):
	"""Parser for tokenized calculator inputs."""

	def parse(self):
		"""Parse calculator input and return the result of evaluating it.

		>>> Parser([1, '*', '(', 2, '+', 3, ')']).parse()
		5
		"""
		return self._parse_expression()

	def _expect(self, char):
		"""Expect a certain character, or raise if it is not next."""
		for _ in self._take(lambda t: t == char):
			return

		raise self._unexpected(char)

	def _unexpected(self, *expected):
		"""Create an exception for an unexpected character."""
		try:
			return UnexpectedCharacterError(self._items.peek(), expected)
		except StopIteration:
			return UnexpectedEndError(expected)


class ParserPartOne(ParserCommon):

	def _parse_expression(self):
		"""Parse an Expression and return the result of evaluating it.

		>>> Parser([1, '+', 2])._parse_expression()
		3
		"""

		# Parse the first (required) Term
		items = [self._parse_item()]

		# Parse any following: ("+"|"*") Item
		op = lambda t: t in '+*'
		items += flatten((op, self._parse_item()) for op in self._take(op))

		return evaluate(items)

	def _parse_item(self):
		"""Parse an Item and return the result of evaluating it.

		>>> Parser([1])._parse_item()
		1

		>>> Parser(['(', 1, '+', 2, '*', 3, ')'])._parse_item()
		9
		"""

		# NOTE: Here's where Python gets a little cumbersome. This isn't really
		#	   a for, we're just using it to handle the case where it doesn't
		#	   find a number (gracefully skip). If it finds one, we return the
		#	   number.
		for n in self._take(lambda t: isinstance(t, int)):
			return n

		# If we failed to parse a number, then try to find a '('
		for _ in self._take(lambda t: t == '('):
			# If we found a '(', parse the subexpression
			value = self._parse_expression()
			# Make sure the subexpression is followed by a ')'
			self._expect(')')
			return value

		# Both parsing the number and subexpresion failed
		raise self._unexpected('number', '(')


class ParserPartTwo(ParserCommon):

	def _parse_expression(self):
		"""Parse an Expression and return the result of evaluating it.

		>>> Parser([1, '+', 2])._parse_expression()
		3
		"""

		# Parse the first (required) Term
		terms = [self._parse_term()]

		# Parse any following: ("+"|"-") Term
		op = lambda t: t in '*'
		terms += flatten((op, self._parse_term()) for op in self._take(op))

		return evaluate(terms)

	def _parse_term(self):
		"""Parse a Term and return the result of evaluating it.

		>>> Parser([1, '*', 2])._parse_term()
		2
		"""

		# Parse the first (required) Factor
		factors = [self._parse_factor()]

		# Parse any following: ("*"|"/") Factor
		op = lambda t: t in '+'
		factors += flatten((op, self._parse_factor()) for op in self._take(op))

		return evaluate(factors)

	def _parse_factor(self):
		"""Parse a Factor and return the result of evaluating it.

		>>> Parser([1])._parse_factor()
		1

		>>> Parser(['(', 1, '+', 2, '*', 3, ')'])._parse_factor()
		7
		"""

		# NOTE: Here's where Python gets a little cumbersome. This isn't really
		#	   a for, we're just using it to handle the case where it doesn't
		#	   find a number (gracefully skip). If it finds one, we return the
		#	   number.
		for n in self._take(lambda t: isinstance(t, int)):
			return n

		# If we failed to parse a number, then try to find a '('
		for _ in self._take(lambda t: t == '('):
			# If we found a '(', parse the subexpression
			value = self._parse_expression()
			# Make sure the subexpression is followed by a ')'
			self._expect(')')
			return value

		# Both parsing the number and subexpresion failed
		raise self._unexpected('number', '(')

def evaluate(items):
	"""
	Evaluate a list of floats separated by operators (at the same level of
	precedence). Returns the result.

	>>> evaluate([3, '*', 4, '/', 2])
	6
	"""

	assert items, 'cannot evaluate empty list'
	# x, x + x, x + x + x, etc. all have an odd number of tokens
	assert len(items) % 2 == 1, 'list must be of odd length'

	while len(items) > 1:
		items = [_evaluate_binary(*items[:3])] + items[3:]

	return items[0]


def _evaluate_binary(lhs, op, rhs):
	"""Evalutates a single binary operation op where lhs and rhs are floats."""
	ops = {'+': operator.add,
		   '*': operator.mul,
	}

	return ops[op](lhs, rhs)
