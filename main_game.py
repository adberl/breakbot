import pygame

pygame.init()
screen = pygame.display.set_mode((300, 450))
working = True
bat_color = (255, 100, 0)
ui_color =  (222,222,222)
rowColors = [(211,111,142), (125,172,177), (175,211,176), (137,114,149)]
x = 120
y = 420

score = 0
time = 0
gen = 0
spec = 0

font = pygame.font.SysFont("andalemono", 45)
text = font.render("S:{} T:{} G:{} SP:{}".format(score, time, gen, spec), True, (0, 0, 0))

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

	
bricks = createBricks(4, rowColors, 120, screen)		
			
while working:

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				working = False
			

	pressed = pygame.key.get_pressed()	
	if pressed[pygame.K_LEFT]: x -= 4
	if pressed[pygame.K_RIGHT]: x += 4


	x = max(min(x, 230), 10)
	
	screen.fill((0, 0, 0))

	
	for brick in bricks:
		brick.drawBrick()
	
	pygame.draw.rect(screen, bat_color, pygame.Rect(x, y, 60, 20))

	pygame.draw.rect(screen, ui_color, pygame.Rect(0, 0, 10, 420)) # left down
	pygame.draw.rect(screen, ui_color, pygame.Rect(0, 0, 300, 80)) # left to right top
	pygame.draw.rect(screen, ui_color, pygame.Rect(290, 0, 10, 420)) # right down
	
	pygame.draw.rect(screen, (120, 20, 20), pygame.Rect(0, 420, 10, 20)) # right down
	pygame.draw.rect(screen, (120, 20, 20), pygame.Rect(290, 420, 10, 20)) # right down

	screen.blit(text, ((300 - text.get_width()) // 2, 20))	
	pygame.display.flip()
	pygame.time.Clock().tick(60)