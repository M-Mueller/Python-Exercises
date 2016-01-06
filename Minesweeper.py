import random
from itertools import product

class Grid:
	def __init__(self, m, n, initial=0):
		self.grid = [[initial for r in range(n)] for c in range(m)]
		self.num_columns = m
		self.num_rows = n

	def __call__(self, x, y):
		return self.grid[x][y]

	def set(self, x, y, value):
		self.grid[x][y] = value

	def neighbors(self, x, y):
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
	grid = Grid(m, n)
	# indices of all fields
	fields = [(c,r) for r in range(grid.num_columns) for c in range(grid.num_rows)]
	# pick numMines random indices from the grid and assign them as mines
	for x,y in random.sample(fields, numMines):
		grid.set(x, y, -1)

	# fill remaining fields with hints about their neighboring fields
	for x,y in fields:
		if grid(x, y) != -1:
			grid.set(x, y, hint(grid, x, y))

	return grid

def hint(mines, x, y):
	if mines(x, y) == -1:
		return -1
	else:
		h = 0
		for a, b in mines.neighbors(x, y):
			if(mines(a, b) == -1):
				h += 1
		return h

def is_solved(mines, flags):
	for y in range(mines.num_rows):
		for x in range(flags.num_columns):
			f, m = flags(x, y), mines(x, y)
			# if any mine is not marked, the game is not solved
			if m == -1 and f != 1:
				return False
	return True

def auto_mark(mines, flags):
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
	if mines(x, y) == -1:
		flags.set(x, y, 2)
		return False
	else:
		flags.set(x, y, 2)
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
