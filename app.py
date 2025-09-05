import pygame
from game.parameters import *
from game.game import GameStation
import sys
import os
import random

def randomColor():
	return colors[random.randint(0, len(colors)-1)]
	
def main():
	global screen, clock, game
	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((0, 0))
	clock = pygame.time.Clock()
	
	os.system('clear')
	game = GameStation(screen, images)
	
	while True:
		game.run(clock)

main()
