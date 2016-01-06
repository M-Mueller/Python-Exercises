import random
from itertools import product

class MineField:
	def __init__(self, n, m, numMines):
		self.grid = [[0 for r in range(m)] for c in range(n)]
		for x,y in random.sample([(c,r) for r in range(m) for c in range(n)], numMines):
			self.grid[x][y] = 1
		self.num_columns = n
		self.num_rows = m

	def hint(self, x, y):
		if self.grid[x][y] == 1:
			return -1
		else:
			h = 0
			for a in range(max(x-1, 0), min(x+2, self.num_columns)):
				for b in range(max(y-1, 0), min(y+2, self.num_rows)):
					if(self.grid[a][b] == 1):
						h += 1
			return h

	def __str__(self):
		s = ''
		for y in range(self.num_rows):
			for x in range(self.num_columns):
				if self.grid[x][y] == 0:
					s += str(self.hint(x, y))
				else:
					s += '*'
			s += '\n'
		return s

if __name__ == '__main__':
	m = MineField(5, 5, 10)
	print(m)
