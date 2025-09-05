import pygame

class Mouse:
	def __init__(self):
		self.events = {
			'move': [pygame.MOUSEMOTION, False],
			'down': [pygame.MOUSEBUTTONDOWN, False],
			'up': [pygame.MOUSEBUTTONUP, False],
			'wheel': [pygame.MOUSEWHEEL, False]
		}
		
	def hasEvent(self, event):
		for [k, v] in self.events.items():
			if event.type == v[0]:
				v[1] == True
				return k
		return False
