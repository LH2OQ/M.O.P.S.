from game.structures import Grid, Cell
from game.parameters import *
import random

def colorFade(_from, to):
	arr = []
	for c in range(3):
		d = to[c] - _from[c]
		if d != 0:
			color = min(int(_from[c] + abs(d) / d * random.randint(0, colorFadeIntensity)), 255)
			color = max(color, 0)
			arr.append(color)
		else:
			arr.append(to[c])
	return arr

class StateMachine:
	def __init__(self, states: int):
		self.blueprint = {'condition': None, 'action': None, 'color': None}
		self.states = {s: self.blueprint.copy() for s in range(states)}
	
	def size(self):
		return len(self.states.keys())
		
class CellularAutomaton:
	def __init__(self, grid: Grid, states):
	 	self.grid = grid
	 	self.grid.fillWithCells()
	 	self.stm = StateMachine(states)
	
	def update(self, screen, events):
		self.handleEvents(events)
		for col in self.grid.grid:
	 		for cell in col:
	 			cell.state = cell.next
	 			if cell.color:
	 				cell.color = colorFade(cell.color, self.stm.states[cell.state]['color'])
	 			cell.draw(screen)#self.stm.states[cell.state]['color']#
	
	def getNeighbours(self, x, y, directions=directions):
	 	d = {}.copy()
	 	for s in range(len(self.stm.states.items())):
	 		d[s] = 0
	 	if self.grid.cellExists(x, y):
	 		g = self.grid.grid
	 		for n in directions:
	 			x1 = (x + directions[n][0])%len(g)
	 			y1 = (y + directions[n][1])%len(g[0])
	 			cell = g[x1][y1]
	 			d.update({cell.state: d[cell.state]+1})
	 	return(d)
	 	
	def handleEvents(self, events):
		for event in events:
			pass
				
class GOL(CellularAutomaton):
	def __init__(self, grid, images=None, mi=2, ma=3, eq=3, states = 2):
	 	super().__init__(grid, states)
	 	self.grid.grid = Grid.__randomMap__(self.grid.grid, self.stm.size()-1)
	 	self.rules = {
	 		'min': mi,
	 		'max': ma,
	 		'equal': eq
	 	}
	 	for i in range(states):
	 		self.stm.states[i].update({ 'color': [black, white][i] })
	
	def update(self, screen, events):
		super().update(screen, events)
		for c in range(len(self.grid.grid)):
			for r in range(len(self.grid.grid[c])):
				cell = self.grid.grid[c][r]
				n = self.getNeighbours(cell.x, cell.y)
				if cell.state == 0:
					if n[1] == self.rules['equal']:
						cell.next = 1
				elif cell.state == 1:
					if self.rules['max'] >= n[1] and self.rules['min'] <= n[1]:
						cell.next = 1
					else:
						cell.next = 0
				if cell.next == 1:
					cell.showImage()

"""
function wfRlz(rule, row) {
    let str = nbr = ""
    while (rule < 0 || rule > 255) {rule = Math.abs(Math.abs(rule) - 255)} //???
    intRule = rule
    rule = (rule >>> 0).toString(2)
    for (let i = 0; i < 8-rule.length; i++) str+=0
    rule = str + rule    
    if (row == 0) {
        let c = byId("c"+row+"."+Math.ceil(x/2))
        c.stateNext = Math.ceil(Math.random() * 3)
        cState(c, (hue+180))
    }
    else {
        for (let i = 0; i < x; i++) {
            let c = byId("c"+row+"."+i)
            const c1 = "c"+(row-1)+"."+i,
                cells = [byId(c1).nbr[6](), c1, byId(c1).nbr[2]()]
for (let j = 0; j < cells.length; j++) {
                const cj = byId(cells[j])
                if ((cj != null && cj.stateNow > 0) 
                || (j == i && i == 0 && byId("c"+(row-1)+"."+(x-1)).stateNow > 0)
                || (j == 2 && i == (x-1) && byId("c"+(row-1)+"."+0).stateNow > 0)) nbr += 1 
                else nbr += 0
            }
            if (i < x-1) nbr += " "
        }        
        nbr = nbr.split(" ")
        for (let i = 0; i < x; i++) {
            let c = byId("c"+row+"."+i), index = 0
            nbr[i] = parseInt(nbr[i].substr(nbr[i].indexOf(1), nbr[i].length), 2)
            for (let j = rule.length-1; j >= 0; j--) {
                if (nbr[i] == index) {
                    if (rule.charAt(j) == 1) {                        
                        c.stateNext = state123()
                    }
                    else c.stateNext = c.stateNow
                }
                index++
            }
            cState(c, (hue+180))
        }
    }
    row++
    if (row == y) {
        wol = false
        //golSpdInt = Math.floor(Math.random()*10000)
        row = 0
        intRule++
    }
    if (wol) setTimeout(() => wfRlz(intRule, row), wolSpdInt)
}
const path = [-1, 1, 1, -1]

function ltAnt(a, b, d) {
    if (!a) a = Math.floor(Math.random()*y), b = Math.floor(Math.random()*x)
    else if (!b) b = Math.floor(Math.random()*x)
    const c = byId("c"+a+"."+b),
        state = () => {return (c.stateNow > 0) ? 0 : state123()},
        dir = () => {return (state() == 0) ? -1 : 1}
    c.stateNext = state()
    cState(c, (hue+180))
    if (!d) d = 0
    d = compare((d + dir()), 4, 0)    
    if (d%2 != 0) b = compare((b + p(path, d)), x, 0)
    else a = compare((a + p(path, d)), y, 0)
    if (lan) setTimeout(() => ltAnt(a, b, d), antSpdInt)
}
function fx(grid) {
    if (cRadius > 100-Math.abs(plsFactor) || cRadius < Math.abs(plsFactor)) plsFactor = -plsFactor
    if (spc > maxSpc-Math.abs(spcFactor) || spc < Math.abs(spcFactor)) spcFactor = -spcFactor
    if (pulse) cRadius += plsFactor/10
    if (space) spc += spcFactor/10
    if (grid != null) grid.style.gridGap = spc+"px"
}
function cState(c, hue) {
    if (hue >= 360) hue = hue-360
    if (c.stateNext < 0) c.stateNext = Math.floor(Math.random()*4)
    if (c.stateNext == 1) c.style.background = "hsla("+hue+", "+saturation+"%, "+light+"%, "+alpha+")"
    else if (c.stateNext == 2) c.style.background = "hsla("+(hue+30)+", "+saturation+"%, "+light+"%, "+alpha+")"
    else if (c.stateNext == 3) c.style.background = "hsla("+(hue+60)+", "+saturation+"%, "+light+"%, "+alpha+")"
    else c.style.background = "transparent"
    c.stateNow = c.stateNext
    c.stateNext = 0
}
"""
