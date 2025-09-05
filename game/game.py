import pygame
import sys
import os
import random
from game.ui import *
from game.parameters import *
from game.structures import Grid
from game.pirates import *
from game.automata import GOL
from game.tictactoe import TTT


class GameStation:
	def __init__(self, screen, sprites, fullscreen = True):
		self._width, self._height = screen.get_size()
		self.width = self._width
		self.height = self._height
		self.fullscreen = False
		if fullscreen:
			self.toggleFullScreen()
		self.ui = UI(screen)
		self.screen = screen
		self.grid = Grid.__fromCellSize__(self.width, self.height, cellSize)
		self.sprites = sprites
		self.direction = None
		self.games = [\
			GOL(self.grid, self.sprites),\
			Crew(self.grid, 7),\
			TTT(self.screen, images=self.sprites)\
		]
		self.gameIndex = 1
		
	def toggleFullScreen(self, size=0):
		if size == 0:
			size = (self._width, self._height)
		if self.fullscreen:
			screen = pygame.display.set_mode(size)
			self.width, self.height = screen.get_size()
			self.fullscreen = False
		else:
			screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.fullscreen = True 
	
	def nextGame(self):
		self.gameIndex = (self.gameIndex+1)%3
		
	def run(self, clock):
		#self.grid.draw(self.screen)
		events = pygame.event.get()
		self.handleEvents(events)
		if self.gameIndex > 0:
			self.screen.fill(black)
		self.games[self.gameIndex].update(self.screen, events)
		clock.tick(FPS)
		pygame.display.update()

	def handleEvents(self, events):
		for event in events:
			if event.type == pygame.QUIT:
				self.quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					self.games[0] = GOL(self.grid)
				elif event.key == pygame.K_f:
					self.toggleFullScreen()
				elif event.key == pygame.K_x:
					self.nextGame()
				elif event.key == pygame.K_ESCAPE:
					self.quit()
	
	def quit(self):
		pygame.quit()
		sys.exit()
