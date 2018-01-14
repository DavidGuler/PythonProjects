from pygame import display, Rect, image, event, init
from pygame.math import Vector2
from pygame.locals import *
import time
import sys
import numpy as np
import math
import os.path

init()

class game_borders():
	DISPLAY_INFO = display.Info()
	SCREEN_SIZE = (DISPLAY_INFO.current_w, DISPLAY_INFO.current_h)
	BORDERS = [Rect(0, 					# left
					0, 
					1, 
					SCREEN_SIZE[1]),
			   Rect(0, 				    # top
					0, 
					SCREEN_SIZE[0], 
					1),
			   Rect(SCREEN_SIZE[0] - 1,  # right
					0, 
					1, 
					SCREEN_SIZE[1]),
			   Rect(0, 					# bottom
					SCREEN_SIZE[1] - 1, 
					SCREEN_SIZE[0], 
					1)]

class angle(object):
	def __init__(self, angle):
		self.angle = angle
		
	@property
	def angle(self):
		return self.__angle

	@property
	def sign(self):
		return self.__sign

	@angle.setter
	def angle(self, value):
		if value == 0:
			self.__sign = 1
		else:
			self.__sign = np.sign(value)

		self.__angle = value

VECTOR = Vector2() # A Vector2 obj for simplifying calculations
KEY_SENSITIVITY = 1 # A const which keeps the influence size of a single user arrow key input.
DIRECTIONS = {K_RIGHT: 0,
			  K_UP: -90,
			  K_LEFT: 180,
			  K_DOWN: 90} # The degree of each direction

IMG_PATH = "img"
HERO_IMG = os.path.join(IMG_PATH, "download.bmp")
DEFAULT_SCREEN_COLOR = (0, 0, 0) # Black
INIT_LOC = (game_borders.SCREEN_SIZE[0]/4, 
			game_borders.SCREEN_SIZE[1]/4)
INIT_SIZE_REDUCTION = (-300, -300)
INIT_SPEED = (1,0)