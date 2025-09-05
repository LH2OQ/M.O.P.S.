from random import randint
from game.parameters import *
from game.utils import *
from game.structures import *

class Pirate(Entity):
	def __init__(self, grid, x, y, size, color=orange, _id=None):
		super().__init__(x, y, size, 1, color)
		self.grid = grid
		self.id = _id
		self.leads = False
		self.follows = None
		self.img = pygame.image.load(images[0])
		self._img = False
		
	def draw(self, screen, show = False):
		if (self.leads):
			self.color = red
		if show:
			self.showImage()
		super().draw(screen)

class Crew:
	def __init__(self, grid, number = 1, direction = None):
		self.members = []
		self.show = True
		self.direction = direction
		self.automate = True#False
		self.grid = grid.grid
		self.pathfinder = Pathfinder(grid.grid)
		for m in range(0, number):
			self.members.append(Pirate(grid, len(grid.grid) - m - 1, len(grid.grid[0]) - 1, cellSize, m))
		self.members[0].leads = True
		for p in range(1, len(self.members)):
			self.members[p].follows = self.members[p-1]
		
		self.target = Vector(randint(0, self.members[0].grid.cols-1), randint(0, self.members[0].grid.rows-1))
	
	def update(self, screen, events):
		leader = self.findLeader()
		src = Vector(leader.x, leader.y)
		dest = self.target
		self.direction = self.nextStep(src, dest, events)
		if self.direction:
			self.move(self.direction)
		for p in self.members:
			p.draw(screen, self.show)
		target = self.members[0].grid.grid[self.target.x][self.target.y]
		tmp = target.color
		target.color = green
		target.draw(screen)
		target.color = tmp
		
	
	def nextStep(self, src, dest, events):
		if self.automate:
			if not src.equals(dest):
				path = self.pathfinder.astar(src, dest)
				if len(path):
					step = path[0]
					x = step.x - src.x
					y = step.y - src.y
					if y != 0:
						return 'S' if y == 1 else 'N'
					elif x != 0:
						return 'E' if x == 1 else 'W'
		return self.handleEvents(events)

	def findLeader(self):
		return list(filter(lambda x: x.leads, self.members))[0]
	
	def move(self, direction):
		leader = self.findLeader()
		if leader.move(direction):
			print('#######', direction)
			for m in self.members:
				if m.follows:
					step = m.getDirection(m.follows.path[-2])
					if step:
						m.move(step)
						print(step)
	
	def handleEvents(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					return 'N'
				elif event.key == pygame.K_DOWN:
					return 'S'
				elif event.key == pygame.K_LEFT:
					return 'W'
				elif event.key == pygame.K_RIGHT:
					return 'E'
				if event.key == pygame.K_a:
					self.automate = not self.automate
		return None
	
	
