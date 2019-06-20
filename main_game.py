import pygame
import math
import random
import numpy
import threading
import time

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
timer = 0
generation = []
gen_id = 0
specimen = 0
spec_id = 0
SPECIMENS_PER_GEN = 15


font = pygame.font.SysFont("andalemono", 45)

bricks = None
ball = None

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
		ypos = math.cos(self.angle) * self.speed
		if ypos <= 0 and ypos >= -1:
			ypos = -1
		self.x += int(math.sin(self.angle) * self.speed)
		self.y -= math.ceil(ypos)
		
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
				
				if distX**2 + distY**2 <= self.size**2 and not brick.destroyed:
					brick.destroyed = True
					global score
					score += 1
					self.x = oldx
					self.y = oldy
					
					if distX <= 0:
						self.angle = math.pi - self.angle 
#						print('bottom or top', math.degrees(self.angle))
					else:
						self.angle = -self.angle		
#						print('hit side', math.degrees(self.angle))					
					break			

			if self.y + self.size > y and (self.x >= x and self.x <= x+60):
				self.y = oldy
				dist = -(x+60 - self.x) + 30
				self.angle = (math.pi-self.angle) + math.radians(dist) #math.pi - self.angle
			
			elif self.y > y:
				print('loser')
				lost()
	
def inc_timer():
	if working:
		global timer
		timer += 1
		time.sleep(1)
		inc_timer()
			
def lost():
	global bricks, ball, timer, score
	bricks = createBricks(4, rowColors, 120, screen)		
	ball = Ball(6, 155, 400, (120, 240, 0), 5)
	score = 0
	timer = 0
	x = 120
	y = 420
	
	# nn stuff:
	

def sigmoid(x):
	return 1 / ( 1 + np.exp(-1 * x))

def relu(x):
    a = x
    a[x < 0] = 0
    return a
	
class Specimen:
	min_weight = -0.1
	max_weight  = 0.1

	def __init__(self, gen, inputs, nr_layer1, nr_layer2):
		self.gen = gen
		self.l1_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(inputs, nr_layer1))
		self.l2_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(nr_layer1, nr_layer2))
		self.out_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(nr_layer2, 1))
		self.fitness = 0
		
	def output(self, input_vector):
		l1_out = np.matmul(input_vector, self.l1_weights)
		l1_out = relu(l1_out)
		l2_out = np.matmul(self.l1_weights, self.l2_weights)
		l2_out = relu(l2_out)
		return sigmoid(np.matmul(self.l2_weights, self.out_weights))

def genZero():
	for i in range(SPECIMENS_PER_GEN):
		generation.append(Specimen(gen_id, 2, 16, 8))
	
def saveGen():
	f = open('gen_'+gen_id,'w')
	for specimen in generation:
		f.write(specimen.l1_weights, specimen.l2_weights, specimen.out_weights, specimen.fitness)
	f.close()

lost()
thtimer = threading.Timer(1.0, inc_timer)
thtimer.start()

genZero():
	
while working:
	if timer == 30:
		print('you reached 30')
		lost()
	if(score == 32):
		print('won')
	if(timer == 0):
		lost()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			working = False
			thtimer.join()		

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

	text = font.render("S:{} T:{} G:{} SP:{}".format(score, timer, gen_id, specimen), True, (0, 0, 0))
	screen.blit(text, ((300 - text.get_width()) // 2, 20))	
	pygame.display.flip()
	pygame.time.Clock().tick(90)
