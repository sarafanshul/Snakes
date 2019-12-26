'''
TODO ->
- add increasing speed
- add good graphics
- add promt cleanup of default texts
- add titlebar change
- 
'''

import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox
import os ,sys
from pygame.locals import *
# initialize
# pygame.init()

width = 500
height = 500

cols = 20
rows = 20

# cols = 25
# rows = 20

class cube():

	# w = 500
	# h = 500
	cols = 20
	rows = 20
	# global width,height,rows,cols
	w = width
	h = height
	
	def __init__(self, start, dirnx=1, dirny=0, color=(241,196,15)):
		self.pos = start
		self.dirnx = dirnx
		self.dirny = dirny # "L", "R", "U", "D"
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
			

	def draw(self, surface, eyes=False):
		# dis = self.w // self.rows
		dis_x = self.w // self.rows
		dis_y = self.h // self.cols

		i = self.pos[0]
		j = self.pos[1]
		
		pygame.draw.rect(surface, self.color, (i*dis_x+1,j*dis_y+1,dis_x-2,dis_y-2))
		if eyes:
			centre = dis_x//2 
			radius = (rows+cols)//30 # add cube size for radius
			circleMiddle = (i*dis_x + centre-radius,j*dis_x+8)
			circleMiddle2 = (i*dis_y + dis_y -radius*2, j*dis_y+8)
			pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
		


class snake():
	body = [] # use deque insted
	turns = {} # default dicts
	
	def __init__(self, color, pos):
		#pos is given as coordinates on the grid ex (1,5)
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
	
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_UP]:
					self.dirny = -1
					self.dirnx = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_DOWN]:
					self.dirny = 1
					self.dirnx = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
		
		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				c.move(c.dirnx,c.dirny)
		
		
	def reset(self,pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy
	
	def draw(self, surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)



def redrawWindow():
	global win
	win.fill((20, 20, 20))
	# drawGrid(width, rows, win)
	drawGrid(width, height, rows, cols, win)
	s.draw(win)
	snack.draw(win)
	pygame.display.update()
	pass



# add sizebtwn X,Y
def drawGrid(w, h, rows, cols ,surface):
	sizeBtwn_X = w // rows
	sizeBtwn_Y = h // cols
	x = 0
	y = 0
	grid_line_col = (69, 69, 71)
	for l in range(rows):
		x = x + sizeBtwn_X
		y = y +sizeBtwn_Y

		pygame.draw.line(surface, grid_line_col, (x, 0),(x,w))
		pygame.draw.line(surface, grid_line_col, (0, y),(w,y))
	


def randomSnack(rows, cols, item):
	positions = item.body

	while True:
		x = random.randrange(1,rows-1)
		y = random.randrange(1,cols-1)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break

	return (x,y)


def main():
	global s, snack, win

	# w = 500 ,h = 500
	win = pygame.display.set_mode((width,height))
	# win = pygame.display.set_mode((width,height) ,RESIZABLE)
	
	# add random in position and change color
	#          (color ,   position)

	color = (255, 242, 0,1.0) # matt Yellow
	position  = (10 ,10) # add random here
	s = snake(color,position)

	s.addCube()
	snack = cube(randomSnack(rows,cols,s), color=(0,255,0))
	flag = True
	clock = pygame.time.Clock()
	
	while flag:
		# delay is ~ refresh rate (default = 10)
		pygame.time.delay(10)
		
		# tick(value) ,value proportional to speed of game(FPS)
		fps = 10
		clock.tick(fps)
		# print(clock.get_fps())

		s.move()
		headPos = s.head.pos
		if headPos[0] >= rows or headPos[0] < 0 or headPos[1] >= cols or headPos[1] < 0:
			print("Score:", len(s.body))
			tk.Tk().wm_withdraw()
			result = messagebox.askokcancel('Restart?' , f'Your Score is {len(s.body)} \nDo you want to Restart the Game ?')
			if result == True: # restart the program using exce function
							# The exec functions of Unix-like operating 
							#   systems are a collection of functions that
							#   causes the running process to be completely 
							#   replaced by the program passed as an argument to the function
				os.execl(sys.executable,sys.executable, *sys.argv)
					# pass
			else:
				pygame.quit()
				exit()
				break

		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows,cols,s), color=(0,255,0))
			
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
				print("Score:", len(s.body))
				tk.Tk().wm_withdraw()
				result = messagebox.askokcancel('Restart?' , f'Your Score is {len(s.body)} \nDo you want to Restart the Game ?')
				if result == True: # restart the program using exce function
							# The exec functions of Unix-like operating 
							#   systems are a collection of functions that
							#   causes the running process to be completely 
							#   replaced by the program passed as an argument to the function
					os.execl(sys.executable,sys.executable, *sys.argv)
					# pass
				else:
					pygame.quit()
					exit()
					break
				# s.reset((10,10))
				# break
					
		redrawWindow()

if __name__ == '__main__':
	main()
