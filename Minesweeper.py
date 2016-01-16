import random
from itertools import product

class Grid:
	'''2D grid of values with m columns and n rows.
	>>> Grid(2, 2)
	0 0
	0 0
	>>> Grid(2, 2, 1)
	1 1
	1 1
	>>> Grid(3, 2)
	0 0 0
	0 0 0
	>>> Grid(2, 3)
	0 0
	0 0
	0 0
	>>> Grid(2,0)
	Traceback (most recent call last):
	...
	ValueError: Grid size cannot be smaller than 1
	>>> Grid(1,-1)
	Traceback (most recent call last):
	...
	ValueError: Grid size cannot be smaller than 1
	>>> g = Grid(3, 4)
	>>> g.num_rows
	4
	>>> g.num_columns
	3
	'''
	def __init__(self, m, n, initial=0):
		if m <= 0 or n <=0:
			raise ValueError('Grid size cannot be smaller than 1')
		self.grid = [[initial for r in range(n)] for c in range(m)]
		self.num_columns = m
		self.num_rows = n

	def __call__(self, x, y):
		'''Returns value at grid point (x, y).
		>>> g = Grid(4, 2)
		>>> g(0, 0)
		0
		>>> g.set(1,1,1)
		>>> g.set(3,0,2)
		>>> g.set(0,1,3)
		>>> g(1,1)
		1
		>>> g(3,0)
		2
		>>> g(0,1)
		3
		>>> g(0,0)
		0
		>>> g(4,0)
		Traceback (most recent call last):
		...
		IndexError: list index out of range
		>>> g(0,4)
		Traceback (most recent call last):
		...
		IndexError: list index out of range
		>>> g(0,-1)
		3
		'''
		return self.grid[x][y]

	def set(self, x, y, value):
		'''Overrides the value at grid point (x, y)
		>>> g = Grid(3, 2)
		>>> g(0,0)
		0
		>>> g.set(0, 0, 4)
		>>> g.set(1, 0, 5)
		>>> g.set(0, 1, 6)
		>>> g
		4 5 0
		6 0 0
		'''
		self.grid[x][y] = value

	def neighbors(self, x, y):
		'''Returns a generator for all neighbors of a grid point (x,y)
		Does not return the central grid point, i.e. (x,y).
		Does not generate points outside the grid for grid points at the border.
		'''
		for a in range(max(x-1, 0), min(x+2, self.num_columns)):
			for b in range(max(y-1, 0), min(y+2, self.num_rows)):
				if a != x or b != y:
					yield (a, b)

	def __str__(self):
		s = ''
		for y in range(self.num_rows):
			for x in range(self.num_columns):
				s += str(self(x,y)) + ' '
			s = s[:-1] + '\n' #remove last space and add newline
		return s[:-1] #remove last newline

	def __repr__(self):
		return str(self)

	@classmethod
	def _test_grid(cls):
		'''
		>>> Grid._test_grid()
		0 3 6 9
		1 4 7 10
		2 5 8 11
		'''
		g = Grid(4,3)
		for i, (x, y) in enumerate(product(range(4), range(3))):
			g.set(x,y,i)
		return g

class Flags:
	Unknown = 0
	Marked = 1
	Revealed = 2

def generate_minefield(m, n, numMines):
	'''Generates a Grid of variable size and a specific number of mines.
	Mines are assigned a value of -1. 
	All other fields are assigned the number of mines in directly neighboring fields.
	For example if a field is surrounded by mines it has a value of 8.
	'''
	grid = Grid(m, n)
	# indices of all fields
	fields = [(c,r) for r in range(grid.num_columns) for c in range(grid.num_rows)]
	# pick numMines random indices from the grid and assign them as mines
	for x,y in random.sample(fields, numMines):
		grid.set(x, y, -1)

	# fill remaining fields with hints about their neighboring fields
	for x,y in fields:
		grid.set(x, y, hint(grid, x, y))

	return grid

def is_mine(mine):
	'''Returns True if the value is a mine.
	'''
	return mine == -1

def hint(mines, x, y):
	'''Returns the number of mines in the neighboring fields or the mine value if the field itself is a mine.
	'''
	if is_mine(mines(x, y)):
		return mines(x, y)
	else:
		h = 0
		for a, b in mines.neighbors(x, y):
			if(mines(a, b) == -1):
				h += 1
		return h

def is_solved(mines, flags):
	'''Returns true if all mines are flagged
	'''
	for y in range(mines.num_rows):
		for x in range(flags.num_columns):
			f, m = flags(x, y), mines(x, y)
			# if any mine is not marked, the game is not solved
			if is_mine(m) and f != Flags.Marked:
				return False
	return True

def auto_mark(mines, flags):
	'''Marks all mines and reveals all fields but only if all non-mine fields are already revealed
	'''
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			f, m = flags(x, y), mines(x, y)
			# check if all non-mine fields are revealed
			if not is_mine(m) and f == Flags.Unknown:
				return False

	# mark all mines and reveal remaining flields
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			if is_mine(mines(x, y)):
				flags.set(x, y, 1)
			else:
				flags.set(x, y, 2)

def reveal(mines, flags, x, y):
	'''Reveals a fields.
	Returns False if the revealed field was a mine field or True otherwise.
	If the revealed field has no neighboring mines all neighboring fields are revealed recursively.
	'''
	flags.set(x, y, Flags.Revealed)
	if is_mine(mines(x, y)):
		return False
	else:
		if mines(x, y) == 0:
			for nx, ny in mines.neighbors(x, y):
				if flags(nx,ny) == Flags.Unknown:
					ok = reveal(mines, flags, nx, ny)
					assert(ok) # must not be surrounded by any mines
		auto_mark(mines, flags)
		return True

def print_field(mines, flags):
	s = ''
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			f, m = flags(x, y), mines(x, y)
			if f == Flags.Unknown:
				s += '?'
			elif f == Flags.Marked:
				s += '!'
			elif f == Flags.Revealed:
				if is_mine(m):
					s += '*'
				else:
					s += str(m)
		s += '\n'
	print s

if __name__ == '__main__':
	import doctest
	doctest.testmod()
	m,n = 5,5
	mines = generate_minefield(m, n, 2)
	flags = Grid(m, n, Flags.Unknown)

	while(True):
		print_field(mines, flags)
		print "Select (Column, Row): ",
		try:
			x, y = input()
		except KeyboardInterrupt:
			print
			break
		except:
			print "Invalid input"
			continue

		if not reveal(mines, flags, x, y):
			print "You Lose!"
			print_field(mines, flags)
			break
		if is_solved(mines, flags):
			print "You Win!"
			print_field(mines, flags)
			break
