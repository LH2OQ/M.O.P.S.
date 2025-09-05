from mouse import Mouse

mouse = Mouse()

black = (0, 0, 0)
white = (255, 255, 255)
red = (128, 0, 0)
orange = (192, 128, 0)
yellow = (128, 128, 0)
ygreen = (128, 192, 0)
green = (0, 128, 0)
gcyan = (0, 192, 0)
cyan = (0, 128, 128)
cblue = (0, 128, 192)
blue = (0, 0, 128)
bviolet = (128, 0, 192)
violet = (128, 0, 128)
vred = (192, 0, 128)

colors = [black, red, orange, yellow, ygreen, green, gcyan, cyan, cblue, blue, bviolet, violet, vred, white]

directions = {
	'N': [0, -1],
	'NE': [1, -1],
	'E': [1, 0], 
	'SE': [1, 1],
	'S': [0, 1],
	'SW': [-1, 1],
	'W': [-1, 0],
	'NW': [-1, -1]
}

_height = 480
_width = 640
cellSize = 150

colorFadeIntensity = 9
FPS = 2

images = ['wallpaper/pirat.png', 'wallpaper/seagulls.png', 'wallpaper/monkeys.png', 'wallpaper/octopus.png']

default_font = ['Comic Sans MS', 72]
