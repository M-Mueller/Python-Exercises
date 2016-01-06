import random
from itertools import product

class Grid:
	'''2D grid of values
	'''
	def __init__(self, m, n, initial=0):
		self.grid = [[initial for r in range(n)] for c in range(m)]
		self.num_columns = m
		self.num_rows = n

	def __call__(self, x, y):
		'''Returns value at grid point (x, y)
		'''
		return self.grid[x][y]

	def set(self, x, y, value):
		'''Overrides the value at grid point (x, y)
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
				s += str(self(x,y))
			s += '\n'
		return s

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

def hint(mines, x, y):
	'''Returns the number of mines in the neighboring fields or -1 if the field itself is a mine.
	'''
	if mines(x, y) == -1:
		return -1
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
			if m == -1 and f != 1:
				return False
	return True

def auto_mark(mines, flags):
	'''Marks all mines as flagged and reveals all fields but only if all non-mine fields are already revealed
	'''
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			f, m = flags(x, y), mines(x, y)
			# check if all non mine fields are revealed
			if m != -1 and f == 0:
				return False

	# mark all mines and reveal remaining flields
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			if mines(x, y) == -1:
				flags.set(x, y, 1)
			else:
				flags.set(x, y, 2)

def reveal(mines, flags, x, y):
	'''Reveals a fields.
	Returns False if the revealed field was a mine field or True otherwise.
	If the revealed field has no neighboring mines all neighboring fields are revealed recursively.
	'''
	flags.set(x, y, 2)
	if mines(x, y) == -1:
		return False
	else:
		if mines(x, y) == 0:
			for nx, ny in mines.neighbors(x, y):
				if flags(nx,ny) == 0:
					ok = reveal(mines, flags, nx, ny)
					assert(ok) # must not be surrounded by any mines
		auto_mark(mines, flags)
		return True

def print_field(mines, flags):
	s = ''
	for y in range(mines.num_rows):
		for x in range(mines.num_columns):
			f, m = flags(x, y), mines(x, y)
			if f == 0:
				s += '?'
			elif f == 1:
				s += '!'
			elif f == 2:
				if m == -1:
					s += '*'
				else:
					s += str(m)
		s += '\n'
	print s

if __name__ == '__main__':
	m,n = 5,5
	mines = generate_minefield(m, n, 2)
	flags = Grid(m, n)

	#print(str(mines).replace('-1', '*'))

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
