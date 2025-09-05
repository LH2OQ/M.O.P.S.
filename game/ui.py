import thorpy as tp

class UI:
	def __init__(self, screen, theme = tp.theme_classic):
		self.screen = screen
		self.elements = []	
		tp.init(screen, theme)
		
	def update(self):
		for element in self.elements():
			element.react(event)
	
	def add(self, element):
		self.elements.append(element)
	
	def remove(self, element):
		if element in self.elements:
			self.elements.remove(element)
	
	def box(self, elements, title = None):
		if title:
			return tp.TitleBox(title, elements)
		
	def slider(self, length, limvals=None, text='', type_=float, initial_value=None):
		return tp.Slider(length, limvals, text, type_, initial_value)
		
	def paramSetter(self, varsets, elements=None, size=None):
		return tp.paramSetter(varsets, elements, size)
