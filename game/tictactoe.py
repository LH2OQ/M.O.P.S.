from game.parameters import *
from game.structures import GridGame, Grid

class TTT(GridGame):
	def __init__(self, screen, images = None, colors = colors):
		self.size = 3
		self.player = 2
		self.match = 3
		super().__init__(screen, self.size, self.player, images, colors, self.player)
		
	def update(self, screen, events):
		super().update(screen)
		self.handleEvents(events, screen)
		self.applyToAll(self.colorChange)
		m = self.getMatches()
		if m:
			self.alert(m, screen)
			self.reset()
			
	def getMatches(self):
		g = self.grid.grid
		m = []
		for i in range(len(g)):
			m.append([c.state for c in g[i]])
		rows = []
		diagonals = []
		for c in range(len(m)):
			for y in list(set(m[c])):
				if m[c].count(y) == self.match and y > 0:
					return f'vertical match: {self.match}x player {y}'
			for r in range(len(m[c])):
				if not len(rows) or len(rows) <= r:
					rows.append([])
				rows[r].append(m[c][r])
		print(rows)
		for x in rows:
			for y in list(set(x)):
				if x.count(y) == self.match and y > 0:
					return f'horizontal match: {self.match}x player {y}'
		for x in Grid.__get_diagonals__(g, self.match):
			x = [g[y[0]][y[1]].state for y in x]
			for y in list(set(x)):
				if x.count(y) == self.match and y > 0:
					print(x)
					return f'diagonal match: {self.match}x player {y}'
		return None
						
	def handleEvents(self, events, screen):
		for event in events:
			e = mouse.hasEvent(event)
			if e:
				if e == 'down':
					state = self.applyToAll(self.checkCellStateOnClick, [list(event.pos)])[0]
					if state[0] == 0:
						cell = state[1]
						self.active_player = (self.active_player+1)%self.player
						cell.state = self.active_player+1
						cell.img = cell.loadImage(images[self.active_player])
						cell._img = cell.keep_img = True
