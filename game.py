# Name: Pranav Polavarapu (ID: 010999511)
# Description: this assignment takes the code that was implemented for the Ms.Pac-man game in Assignment 5 in Java and ports it over into Python. This project makes use of all five sprites (walls, Ms. Pac-man, fruits, ghosts, and pellets).
# Due: May 2nd, 2024 

import pygame
import time
import json

from pygame.locals import*
from time import sleep

class Sprite(): #sprite class 
	def __init__(self, x, y, w, h, image):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.image = pygame.image.load(image)

	def draw(self, screen, scrollAmount): #draw method, derived from the code provided
		LOCATION = (self.x, self.y - scrollAmount)
		SIZE = (self.w, self.h)
		screen.blit(pygame.transform.scale(self.image, SIZE), LOCATION)

	def update(self): #update method
		pass

class Wall(Sprite): #wall class
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h, "wall.png") #using super to access parent constructor

class Pellet(Sprite): #pellet class
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h, "Pellet.png") #using super to access parent constructor

class Fruit(Sprite): #fruit class
	def __init__(self, x, y, w, h, direction):
		super().__init__(x, y, w, h, "fruit2.png") #using super to access parent constructor
		self.direction = direction #specifically setting the additional direction parameter

class Ghost(Sprite): #ghost class
	def __init__(self, x, y, w, h, collided, imageName, animationTime):
		super().__init__(x, y, w, h, "ghost.png") #using super to access parent constructor
		self.collided = collided #specifically setting the collided parameter
		self.imageName = imageName #specifically setting the imageName parameter for the ghost
		self.animationTime = animationTime #specifically setting the animationTime parameter for the time intervals in the animation for the ghost

class Pacman(Sprite): #pacman class
	def __init__(self, x, y, imageIndex):
		super().__init__(x, y, 50, 50, "pacman7.png") #using super to access parent constructor
		self.imageIndex = imageIndex #specifically setting the imageIndex parameter

	def move(self, x, y): #pacman move method
		self.x += x
		self.y += y
	
	def goUp(self): #goUp method for pacman animation
		if (self.imageIndex == 4):
			self.imageIndex = 5
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		elif (self.imageIndex == 5): 
			self.imageIndex = 6
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		else:
			self.imageIndex = 4
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")

	def goDown(self): #goDown method for pacman animation
		if (self.imageIndex == 10):
			self.imageIndex = 11
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		elif (self.imageIndex == 11): 
			self.imageIndex = 12
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		else:
			self.imageIndex = 10
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")

	def goRight(self): #goRight method for pacman animation
		if (self.imageIndex == 7):
			self.imageIndex = 8
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		elif (self.imageIndex == 8): 
			self.imageIndex = 9
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		else:
			self.imageIndex = 7
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")

	def goLeft(self): #goLeft method for pacman animation
		if (self.imageIndex == 1):
			self.imageIndex = 2
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		elif (self.imageIndex == 2): 
			self.imageIndex = 3
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")
		else:
			self.imageIndex = 1
			self.image = pygame.image.load("pacman" + str(self.imageIndex) + ".png")

class Model(): #model class
	def __init__(self): 
		self.sprites = [] #empty sprites array to hold sprites
		self.pacman = Pacman(250, 500, 7) #setting pacman
		self.sprites.append(self.pacman) #adding pacman to sprites array
		
		#calling loadJson helper method to load information from the json file
		self.loadJson()

	def movePacman(self, x, y):
		self.pacman.move(x, y)

	def makePellet(self, x, y): #method to create pellet
		pellet = Pellet(x, y, 15, 15)
		self.sprites.append(pellet) #adding created pellet to sprites array
	
	def makeFruit(self, x, y): #method to create fruit
		fruit = Fruit(x, y, 25, 25, 0)
		self.sprites.append(fruit) #adding created fruit to sprites array

	def makeGhost(self, x, y): #method to create ghost
		ghost = Ghost(x, y, 35, 35, False, "ghost.png", 100) #setting default values for parameters
		self.sprites.append(ghost) #adding created ghost to sprites array

	def detectCollisionGeneric(self, a, b): #detecting collision, helper method; same coding logic as in my previous java program
		leftBoundaryA = a.x
		rightBoundaryA = a.x + a.w
		topBoundaryA = a.y
		bottomBoundaryA = a.y + a.h

		leftBoundaryB = b.x
		rightBoundaryB = b.x + b.w
		topBoundaryB = b.y
		bottomBoundaryB = b.y + b.h

		if ((rightBoundaryB < leftBoundaryA) or (leftBoundaryB > rightBoundaryA) or (bottomBoundaryB < topBoundaryA) or (topBoundaryB > bottomBoundaryA)):
			return False #there is no collision
		else:
			return True #there is a collision
	
	def detectCollisionWithSprites(self, movingObj): #this function, taking in parameters, is used to return the sprite that collides with pacman or fruit for the detectCollision() function below (same logic as with Java program)
		for sprite in self.sprites: 
			if (sprite == movingObj):
				continue
			if (self.detectCollisionGeneric(sprite, movingObj)): #calling method which returns a boolean value for if there is a collision between two sprites
				return sprite #return the colliding sprite
		return None #no collision
	
	def detectCollision(self): #main collision detection method
		sprite = self.detectCollisionWithSprites(self.pacman) #calling helper method which takes pacman as parameter
		if sprite != None: #if there is a collision
			if isinstance(sprite, Pellet) or isinstance(sprite, Fruit): #if pacman collided with a pellet or fruit
				self.sprites.remove(sprite) #remove sprite
				return False
			elif isinstance(sprite, Ghost) and sprite.collided == False: #if pacman collided with a ghost for the first time
				sprite.image = pygame.image.load("vulGhost.png") #changing image to begin death animation
				sprite.imageName = "vulGhost.png"
				sprite.collided = True; #setting collided to true
				return False
			elif isinstance(sprite, Ghost) and sprite.collided == True: #if pacman collided with a ghost which has already been collided with, pass through
				return False
			return True
		return False

	def animateFruits(self): #method used for fruit movement
		for sprite in self.sprites:
			if isinstance(sprite, Fruit):
				fruit = sprite
				collisionSprite = self.detectCollisionWithSprites(fruit) #find what fruit has collided with, if anything
				if collisionSprite != None and isinstance(collisionSprite, Wall): #if fruit collided with a wall
					#reverse direction
					if fruit.direction == 0:
						fruit.direction = 1
					else:
						fruit.direction = 0

				#change X-value of fruit depending on direction
				if fruit.direction == 0:
					fruit.x += 5
					if fruit.x >= 500:
						fruit.x = 0
				else:
					fruit.x -= 5
					if fruit.x <= 0:
						fruit.x = 500

	def animateGhosts(self): #method used for ghost animation cycle
		for sprite in self.sprites:
			if isinstance(sprite, Ghost) and sprite.collided: #if ghost has been collided with
				if sprite.imageName == "vulGhost.png": #if it is on this image of the animation cycle
					sprite.animationTime -= 5
					if sprite.animationTime <= 50: #creating delay between animation images
						sprite.image = pygame.image.load("pacEyes.png") #load next image in the animation
						sprite.imageName = "pacEyes.png" 
				elif sprite.imageName == "pacEyes.png": #if it is on this image of the animation cycle
					sprite.animationTime -= 5
					if sprite.animationTime <= 0: #creating delay between animation images
						self.sprites.remove(sprite) #remove ghost, end of animation cycle

	def update(self):
		#calling necessary fruit and ghost methods
		self.animateFruits()
		self.animateGhosts() 

	def loadJson(self): #helper method to reduce code duplication -- much of the code was already given
		with open("map.json") as file:
			data = json.load(file)
			walls = data["walls"]
			pellets = data["pellets"]
			fruits = data["fruits"]
			ghosts = data["ghosts"]
		file.close()

		for entry in walls:
			self.sprites.append(Wall(entry["x"], entry["y"], entry["w"], entry["h"]))
		for entry in pellets:
			self.sprites.append(Pellet(entry["x"], entry["y"], entry["w"], entry["h"]))
		for entry in fruits:
			self.sprites.append(Fruit(entry["x"], entry["y"], entry["w"], entry["h"], 0)) #setting all fruits to a default direction of 0
		for entry in ghosts:
			self.sprites.append(Ghost(entry["x"], entry["y"], entry["w"], entry["h"], False, "ghost.png", 100)) #setting all ghosts to a default collision value of False, and with a default animationTime of 100

	def reload(self): #method used to reload the map based on the json file 
		self.sprites.clear()
		self.sprites.append(self.pacman)	
		self.loadJson()


class View():
	def __init__(self, model):
		screen_size = (500, 1000)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.scrollAmount = 0

	def update(self):
		self.screen.fill([0,0,26])
		for sprite in self.model.sprites:
			sprite.draw(self.screen, self.scrollAmount)
		pygame.display.flip()

	def scroll(self, scrollAmountChange): #method to adjust the scrolling variable 
		self.scrollAmount += scrollAmountChange

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		#creating necessary variables
		self.keep_going = True
		self.speed = 10
		self.collisionDetected = False
		self.keyLeft = False
		self.keyRight = False
		self.keyUp = False
		self.keyDown = False
		self.keyE = False
		self.keyP = False
		self.keyL = False
		self.keyG = False
		self.keyF = False

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.keep_going = False

			elif event.type == pygame.MOUSEBUTTONUP: #for when a click is made
				if self.keyP == True: #creating pellet on the screen at the cursor's position
					posX, posY = pygame.mouse.get_pos()
					self.model.makePellet(posX, posY + self.view.scrollAmount)

				if self.keyG == True: #creating ghost on the screen at the cursor's position
					posX, posY = pygame.mouse.get_pos()
					self.model.makeGhost(posX, posY + self.view.scrollAmount)

				if self.keyF == True: #creating fruit on the screen at the cursor's position
					posX, posY = pygame.mouse.get_pos()
					self.model.makeFruit(posX, posY + self.view.scrollAmount)

			elif event.type == pygame.KEYUP: #this is keyReleased!
				if event.key == K_e: #toggling in and out of edit mode
					if (self.keyE):
						self.keyE = False
						self.keyP = False
						self.keyG = False
						self.keyF = False
						print("\nOut of edit mode")
					else:
						self.keyE = True
						print("\nIn edit mode")

				if event.key == K_p: #toggling into add pellet mode
					if self.keyE == True:
						self.keyP = True
						self.keyG = False
						self.keyF = False
						print("\nIn add pellet mode")
				
				if event.key == K_l: #loading default json map
					self.keyL = True
					self.model.reload()
					print("\nLoading map")

				if event.key == K_g: #toggling into add ghost mode
					if self.keyE == True:
						self.keyG = True
						self.keyF = False
						self.keyP = False
						print("\nIn add ghost mode")

				if event.key == K_f: #toggling into add fruit mode
					if self.keyE == True:
						self.keyF = True
						self.keyG = False
						self.keyP = False
						print("\nIn add fruit mode")

		
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]: #moving pacman to the left, changing animation accordingly, accounting for horizontal warping, and dealing with collisions
			self.model.movePacman(-self.speed,0)
			self.model.pacman.goLeft()
			if self.model.pacman.x + self.model.pacman.w <= 0:
				self.model.pacman.x = 500 - self.model.pacman.w
			self.keyLeft = True
			if self.model.detectCollision():
				self.model.movePacman(self.speed, 0)

		if keys[K_RIGHT]: #moving pacman to the right, changing animation accordingly, accounting for horizontal warping, and dealing with collisions
			self.model.movePacman(self.speed,0)
			self.model.pacman.goRight()
			if self.model.pacman.x >= 500:
				self.model.pacman.x = 0
			self.keyRight = True
			if self.model.detectCollision():
				self.model.movePacman(-self.speed, 0)

		if keys[K_UP]: #moving pacman up, changing animation accordingly, scrolling, and dealing with collisions
			self.model.movePacman(0,-self.speed)
			self.model.pacman.goUp()
			self.view.scroll(-10)
			self.keyUp = True
			if self.model.detectCollision():
				self.model.movePacman(0, self.speed)
				self.view.scroll(10)

		if keys[K_DOWN]: #moving pacman down, changing animation accordingly, scrolling, and dealing with collisions
			self.model.movePacman(0,self.speed)
			self.model.pacman.goDown()
			self.view.scroll(10)
			self.keyDown = True
			if self.model.detectCollision():
				self.model.movePacman(0, -self.speed)
				self.view.scroll(-10)

print("\n-----------------------------------------------")
print("Use the arrow keys to move. Press Esc to quit.")
print("\nToggle into edit mode by pressing 'e'")
print("\nAdd pellets by pressing 'p' when in edit mode")
print("\nAdd ghosts by pressing 'g' when in ghost mode")
print("\nAdd fruits by pressing 'f' when in fruit mode")
print("-----------------------------------------------")

pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)

print("\nGoodbye")