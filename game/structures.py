import pygame
import random
from game.parameters import *
from game.utils import Vector

class Cell:
	def __init__(self, x, y, size=cellSize, state=0, color=cyan):
		self.x = x
		self.y = y
		self.size = size
		self.pos = Vector(x*self.size, y*self.size)
		self.state = state
		self.color = color
		self.next = self.state
		self.img = self.loadImage(random.choice(images))
		self._img = False
		self.keep_img = False

	def draw(self, screen):
		x = self.pos.x
		y = self.pos.y
		rect = pygame.Rect(x , y, self.size, self.size)
		if self.color:
			pygame.draw.rect(screen, self.color, rect)
		if self._img:
			img = pygame.transform.scale(self.img, (self.size, self.size))
			screen.blit(img, (x, y))
			if not self.keep_img:
				self._img = False
			
	def loadImage(self, img):
		return pygame.image.load(img)
	
	def showImage(self):
		self._img = True
		
class Object(Cell):
	def __init__(self, x, y, size, state, color):
		super().__init__(x, y, size, state, color)
		self.path = [Vector(self.y, self.y)]
		
	def move(self, direction):
		dx = directions[direction][0]
		dy = directions[direction][1]
		possible = direction and self.grid.cellExists(self.x + dx, self.y + dy)
		if possible:
			self.x += dx
			self.y += dy
			self.pos.x += dx * self.size
			self.pos.y += dy * self.size
			self.path.append(Vector(self.x, self.y))
		return possible
			
	def getDirection(self, pos):
		if pos:
			x = pos.x - self.x
			x = abs(x)/x if x != 0 else 0
			y = pos.y - self.y
			y = abs(y)/y if y != 0 else 0
			for k, v in directions.items():
				if v == [int(x), int(y)]:
					return k
		return False
		
		
class Entity(Object):
	def __init__(self, x, y, size, state, color):
		super().__init__(x, y, size, state, color)
	

class Grid:
	def __init__(self, cols, rows, states=2, fill=cyan, stroke=blue, cellSize=cellSize):
		self.grid = []
		self.cols = cols
		self.rows = rows
		self.fill = fill
		self.stroke = stroke
		self.cellSize = cellSize
		self.states = states
		for x in range(0, cols):
			self.grid.append([])
			for y in range(0, rows):
				self.grid[x].append(None)
	
	def fillWithCells(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				self.grid[x][y] = Cell(x, y, size=self.cellSize, color=self.fill)
	
	def cellExists(self, x, y):
		return x >= 0 and y >= 0 and x < len(self.grid) and y < len(self.grid[x])
	
	def draw(self, screen, offset=Vector(0, 0), stroke=True, fill=False):
		if fill:
			screen.fill(self.fill)
		for x in range(0, len(self.grid)):
			for y in range(0, len(self.grid[x])):
				cell = self.grid[x][y]
				cell.pos.x = offset[0]+x*cell.size
				cell.pos.y = offset[1]+y*cell.size
				cell.draw(screen)
				if stroke:
					rect = pygame.Rect(cell.pos.x , cell.pos.y, cell.size, cell.size)
					pygame.draw.rect(screen, self.stroke, rect, 1)
				
	def __empty__(cols, rows):
		grid = []
		for x in range(cols):
			grid.append([])
			for y in range(rows):
				grid[x].append([])
		return grid
		
	def __fromCellSize__(width, height, size):
		return Grid(round(width/size), round(height/size))
		
	def __randomMap__(grid, states=2):
		index = 0
		for col in range(len(grid)):
			for row in range(len(grid[col])):
				grid[col][row] = Cell(col, row, cellSize, random.randint(0, states))
		return grid
		
	def __get_diagonals__(grid, n):
		a = []
		b = []
		cols = len(grid)
		rows = len(grid[0])
		for x in range(cols-(n-1)):
			a.append([])
			b.append([])
			for y in range(x, cols):
				if y < rows:
					a[x].append([x+y, y])
					b[x].append([cols-1-y, y])
		return [*a, *b]
		


class GridGame:
	def __init__(self, screen, size=3, states=2, images=None, colors=colors, player=1):
		self.size = size
		self.images = images
		self.colors = [colors[c] for c in range(size+1)]
		w, h = screen.get_size()
		self.center = (w/2, h/2)
		self.cellSize = self.fitSize(w, h, size)
		half = self.size*self.cellSize/2
		self.start = (self.center[0]-half, self.center[1]-half)
		self.end = (self.center[0]+half, self.center[1]+half)
		self.grid = Grid(size, size, states=states, cellSize=self.cellSize, fill=self.colors[0])
		self.player = player
		self.active_player = -1
		self.grid.fillWithCells()
		
	def update(self, screen):
		self.grid.draw(screen, offset=self.start)
	
	def getCenter(self, screen):
		w, h = screen.get_size()
		return (w/2, h/2)
		
	def fitSize(self, w, h, size, margin_factor=1.25):
		return min(w, h) / size / margin_factor
		
	def applyToAll(self, function, args=[]):
		arr = []
		for x in range(self.size):
			for y in range(self.size):
				arr.append(function(self.grid.grid[x][y], *args))
		return list(filter(None, arr))
	
	def checkCellStateOnClick(self, cell, pos, state:int=None):
		x = pos[0]
		y = pos[1]
		cx = self.start[0] + cell.x * cell.size
		cy = self.start[1] + cell.y * cell.size
		if x > cx and x < cx + cell.size and y > cy and y < cy + cell.size:
			return [cell.state, cell]
		return None
			
	def changeCellStateOnClick(self, cell, pos, state:int=None):
		x = pos[0]
		y = pos[1]
		cx = self.start[0] + cell.x * cell.size
		cy = self.start[1] + cell.y * cell.size
		if x > cx and x < cx + cell.size and y > cy and y < cy + cell.size:
			cell.state = (cell.state+1)%self.grid.states if not state else state
			return cell
		return None
	
	def reset(self):
		self.applyToAll(self.stateChange)
		self.applyToAll(self.set_img)
	
	def set_img(self, cell, img=None):
		cell.img = img
		if not img:
			cell._img = False
		
	def stateChange(self, cell, state=0):
		cell.state = state

	def colorChange(self, cell):
		cell.color = self.colors[cell.state]
		
	def font(self, f):
		return pygame.font.SysFont(*f)
		
	def alert(self, msg, screen, color=white):
		f = self.font(default_font)
		text = f.render(msg, False, color)
		screen.blit(text, self.getCenter(screen))
