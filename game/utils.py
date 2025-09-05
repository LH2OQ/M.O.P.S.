class Vector:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
		self.pos =[x, y]
		
	def equals(self, vec):
		return self.x == vec.x and self.y == vec.y

class Gridnode:
	def __init__(self, x: int, y: int, state=None):
		self.x = x
		self.y = y
		self.f = 0
		self.g = 0
		self.h = 0
		self.nbrs = []
		self.parent = None
	
	def updateNbrs(self, grid):
		x = self.x
		y = self.y
		if x > 0:
			self.nbrs.append(grid[x - 1][y]) 		#left
		else:
			self.nbrs.append(None)
#		if x > 0 and y > 0:
#			self.nbrs.append(grid[x - 1][y - 1])	#top-left
#		else:
#			self.nbrs.append(None)
		if y > 0:
			self.nbrs.append(grid[x][y - 1])		#top
		else:
			self.nbrs.append(None)
#		if x < len(grid) - 1 and y > 0:
#			self.nbrs.append(grid[x + 1][y - 1])	#top-right
#		else:
#			self.nbrs.append(None)
		if x < len(grid) - 1:
			self.nbrs.append(grid[x + 1][y])		#right
		else:
			self.nbrs.append(None)
#		if x < len(grid) - 1 and y < len(grid[x]) - 1:
#			self.nbrs.append(grid[x + 1][y + 1])	#bottom-right
#		else:
#			self.nbrs.append(None)
		if y < len(grid[x]) - 1:
			self.nbrs.append(grid[x][y + 1])		#bottom
		else:
			self.nbrs.append(None)
#		if x > 0 and y < len(grid[x]) - 1:
#			self.nbrs.append(grid[x - 1][y + 1])	#bottom-left
#		else:
#			self.nbrs.append(None)

class Pathfinder:
	def __init__(self, grid):
		self.area = self.initialize(grid)
		
	def initialize(self, grid):
		x = len(grid)
		y = len(grid[0])
		area = [[None] * y] * x
		for i in range(x):
			for j in range(y):
				area[i][j] = Gridnode(i, j)
				a = area[i][j]
				a.state = grid[i][j].state
		for i in range(x):
			for j in range(y):
				area[i][j].updateNbrs(area)
		return area
	
	def heuristic(self, a, b):
		return abs(b.x - a.x) + abs(b.y - a.y)
	
	def astar(self, src, dest):
		visited = []
		start = self.area[src.x][src.y]
		end = self.area[dest.x][dest.y]
		queue = [start]
		path = [Vector(start.x, start.y)]
		while len(queue) > 0:
			lowest = 0
			for i in range(len(queue)):
				if queue[i].f < queue[lowest].f:
					lowest = i
			current = queue[lowest]
			if current == end:
				tmp = current
				path.append(Vector(tmp.x, tmp.y))
				while tmp.parent:
					tmp = tmp.parent
					path.append(Vector(tmp.x, tmp.y))
				path = list(reversed(path))[1:]
				print(start.x, start.y)
				print(end.x, end.y)
				print(path[0].x, path[0].y)
				return path
			del queue[lowest]
			visited.append(current)
			nbrs = current.nbrs
			for i in range(len(nbrs)):
				n = nbrs[i]
				#before = None
				#after = None
				#if i % 2 == 0:
				#	before = nbrs[i - 1];
				#	after = nbrs[(i+1)%len(nbrs)]
				if n and not n.state and not n in visited: #and not before and not after:
					possibleG = current.g + 1
					if not n in queue:
						queue.append(n)
					elif possibleG >= n.g:
						continue
					n.g = possibleG
					n.h = self.heuristic(n, dest)
					n.f = n.g + n.h
					n.parent = current
		return []
