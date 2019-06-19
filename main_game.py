import pygame
import math
import random

pygame.init()

width = 300
height = 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('breakbot')
working = True
going_up = True

#colors
bat_color = (255, 100, 0)
ui_color =  (222,222,222)
rowColors = [(211,111,142), (125,172,177), (175,211,176), (137,114,149)]
background_color = (0, 0, 0)

x = 120
y = 420

score = 0
time = 0
gen = 0
spec = 0

font = pygame.font.SysFont("andalemono", 45)

class Brick:
	size_x = 35
	size_y = 20

	def __init__(self, x, y, col, screen):
		self.x = x
		self.y = y
		self.col = col
		self.screen = screen
		self.destroyed = False

	def drawBrick(self):
		if not self.destroyed:
			pygame.draw.rect(self.screen, 
				self.col, pygame.Rect(self.x, self.y, Brick.size_x, Brick.size_y))

def createBricks(rows, colors, starty, scr):
	if len(colors) < rows:
		print('not enough colors')
		return
	bricks = []
	for row in range(0, rows):
		for col in range(0, 8):
			bricks.append(Brick(
				col*Brick.size_x+10, starty + row * Brick.size_y, colors[row], scr))
	return bricks

class Ball:
	
	def __init__(self, size, x, y, col, speed):
		self.size = size
		self.x = x
		self.y = y
		self.col = col
		self.angle = random.uniform(-math.pi/2, math.pi/2)
		self.speed = speed
			
	def drawBall(self):
		pygame.draw.circle(screen, self.col, (self.x, self.y), self.size)
	
	def move(self):
		oldx = self.x
		oldy = self.y
		self.x += math.ceil(math.sin(self.angle) * self.speed)
		self.y -= math.ceil(math.cos(self.angle) * self.speed)
		
		if self.x + self.size > width-10: # hit right wall
			self.x = self.x - (self.x + self.size - (width-10))
			self.angle = -self.angle		
		elif self.x - self.size < 10: # hit left wall
			self.x = self.x + (self.size - self.x) + 10	
			self.angle = -self.angle
		elif self.y - self.size < 80: # hit top wall
			self.y = self.y + (80 - self.y + self.size)	
			self.angle = math.pi - self.angle
			going_up = False
		else:
		
			for brick in bricks:
				distX = self.x - max(brick.x, min(self.x, brick.x+Brick.size_x))		
				distY = self.y - max(brick.y, min(self.y, brick.y+Brick.size_y))		
				
				if distX**2 + distY**2 < self.size**2 and not brick.destroyed:
					brick.destroyed = True
					global score
					score += 1
					
					if distX <= 0:
						self.angle = math.pi - self.angle 	
					else:
						self.angle = -self.angle							
					break			

			if self.y + self.size > y and (self.x >= x and self.x <= x+60):
				self.y = oldy
				dist = -(x+60 - self.x) + 30
				self.angle = (math.pi-self.angle) + math.radians(dist) #math.pi - self.angle
			
			elif self.y > y:
				print('loser')
				global working
				working = False
				


bricks = createBricks(4, rowColors, 120, screen)		
ball = Ball(6, 150, 400, (120, 240, 0), 5)
			
while working:

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				working = False			

	pressed = pygame.key.get_pressed()	
	if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: x -= 4
	if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]: x += 4

	x = max(min(x, 230), 10)
	
	screen.fill(background_color)

	for brick in bricks:
		brick.drawBrick()
	
	ball.drawBall()
	ball.move()
	
	pygame.draw.rect(screen, bat_color, pygame.Rect(x, y, 60, 20))

	pygame.draw.rect(screen,
		ui_color, pygame.Rect(0, 0, 10, 420)) # left down
	pygame.draw.rect(screen,
		ui_color, pygame.Rect(0, 0, 300, 80)) # left to right top
	pygame.draw.rect(screen,
		ui_color, pygame.Rect(290, 0, 10, 420)) # right down
	pygame.draw.rect(screen,
		(120, 20, 20), pygame.Rect(0, 420, 10, 20)) # right bumper
	pygame.draw.rect(screen,
		(120, 20, 20), pygame.Rect(290, 420, 10, 20)) # left left

	text = font.render("S:{} T:{} G:{} SP:{}".format(score, time, gen, spec), True, (0, 0, 0))
	screen.blit(text, ((300 - text.get_width()) // 2, 20))	
	pygame.display.flip()
	pygame.time.Clock().tick(60)
