'''
Chelone is a graphics library created specifically for our platformer
It is a wrapper over the included tkinter library that seeks to become an
alternative to pyGame with more of a focus on sprites rather then primitives

The engine includes basic loading, collision detection, animation, drawing, z-layering and complex backrounds
'''
import tkinter as tk
from typing import Union, Callable
from time import time, sleep

TARGET_FPS = 60
InFocus = True

def init(resolution_x:int, resolution_y:int):
	# Create the window with the Tk class
	root = tk.Tk()
	
	root.bind("<Key>", on_key_press)
	root.bind("<KeyRelease>", on_key_release)
	root.bind("<FocusIn>", FocusIn)
	root.bind("<FocusOut>", FocusOut)

	# Create the canvas and make it visible with pack()
	canvas = tk.Canvas(root, width=resolution_x, height=resolution_y)
	canvas.pack() # this makes it visible

	clear_img = tk.PhotoImage(file="sprites/clear.png")

	return SpriteRenderer(root,canvas)


def FocusIn(event):
	global InFocus
	InFocus = True

# Function that handles cleaning up our input after window goes out of focus
def FocusOut(event):
	global InFocus, pressed_keys, caught_keys
	InFocus = False
	pressed_keys = []
	caught_keys = []


caught_keys_prev = []
caught_keys= []

pressed_keys = []

clear_img = None

def check_keys():
	global caught_keys_prev, caught_keys, pressed_keys
	# remove keys not caught for 2 frames
	for key in pressed_keys:
		if key not in caught_keys and\
		  key not in caught_keys_prev:

			pressed_keys.remove(key)

	for key in caught_keys:
		if key not in pressed_keys:
			pressed_keys.append(key)

	caught_keys_prev = caught_keys.copy()

def on_key_press(event):
	global caught_keys
	caught_keys.append(event.keysym)


def on_key_release(event):
	global caught_keys
	caught_keys.remove(event.keysym)



class Sprite():
	"""Object that contains data about the sprite. Also can be used to have code ran on each frame"""
	x = 0
	y = 0
	var = {}
	image = None
	image_tk = None
	parent_canvas = None
	updateFunc = None
	_passedUpdateFunc=None
	_in_anim = False
	
	def __init__(self, image:Union[str, tk.PhotoImage], x:int=0, y:int=0, updateFunc:Callable[..., None]=lambda a:None, setupFunc:Callable[..., None]=lambda a:None):
		self.x = x
		self.y = y
		self.var = {}

		if isinstance(image, str):
			self.image = tk.PhotoImage(file=image)
		else:
			self.image = image
		self.image_tk = None
		self.parent_canvas = None
		self._passedUpdateFunc = updateFunc
		self.updateFunc = updateFunc
		self._in_anim = False

		setupFunc(self)

	def move(self, x:int, y:int):
		self.x += x
		self.y += y
		self.parent_canvas.move(self.image_tk, x, y)

	def change_image(self, image:tk.PhotoImage, stop_anim:bool=True):

		if stop_anim and self._in_anim:
			self.updateFunc = self._passedUpdateFunc

		self.image = image
		self.parent_canvas.itemconfig(self.image_tk, image=self.image)


	def shedule_anim(self, anim_frames:list):
		global clear_img

		self._in_anim = True

		i = 0
		tmp = self._passedUpdateFunc
		
		def anim_sheduler(sprite):
			nonlocal i, tmp

			sprite.change_image(anim_frames[i],False)
			i+=1

			if i == len(anim_frames):
				i = 0

			tmp(sprite)

		self.updateFunc = anim_sheduler

class SpriteRenderer():
	"""Main drawing class. Handles drawing every sprite"""
	_root = None
	_screen = None
	_sprites = []
	_prev_draw_time = None

	def __init__(self, root: tk.Tk, screen:tk.Canvas):
		self._root = root
		self._screen = screen
		
		# 50 different z layers
		self._sprites = []
		for i in range(50):
			self._sprites.append([])

	def draw_gui(self):
		pass


	frame_period=1.0/TARGET_FPS
	now=time()
	next_frame=now+frame_period

	def advance_frame(self):

		while self.now<self.next_frame:
			sleep(self.next_frame-self.now)
			self.now=time()

		for layer in self._sprites:
			for sprite in layer:

				sprite.updateFunc(sprite)


		self._root.update()
		self.next_frame+=self.frame_period

	def move_camera(self, x, y):
		self._screen.move("all",x,y)

	def add_sprite(self, sprite:Sprite, layer:int = 25):
		
		#layer 0 reserved for gui, layer 50 onward does not exist
		if layer < 1 or layer > 49:
			return

		self._sprites[layer].append(sprite)

		sprite.image_tk = self._screen.create_image(sprite.x, sprite.y, anchor=tk.NW, image=sprite.image)
		sprite.parent_canvas = self._screen

		for i, z_layer in enumerate(self._sprites):
			if len(z_layer)>0 and i<=layer:
				self._screen.tag_raise(sprite.image_tk, z_layer[0].image_tk)

	def bind(func:Callable, key:str):
		self._root.bind(func,key)

# setting up a basic scene to test
a = init(1000,500)

a.add_sprite(Sprite("Untitled.png",10,10),40)


flag = True
main_anim = [tk.PhotoImage(file = "sprites/1.png"), tk.PhotoImage(file = "sprites/2.png"), tk.PhotoImage(file = "sprites/2.png"), tk.PhotoImage(file = "sprites/2.png"), tk.PhotoImage(file = "sprites/2.png")]
def move(sprite):
	global pressed_keys,flag, main_anim

	if 'w' in pressed_keys:
		sprite.move(0,-1)
	if 'a' in pressed_keys:
		sprite.move(-1,0)
	if 's' in pressed_keys:
		sprite.move(0,1)
	if 'd' in pressed_keys:
		sprite.move(1,0)

	if "q" in pressed_keys:
		sprite.shedule_anim(main_anim)
		flag = False

	if "e" in pressed_keys:
		sprite.change_image(tk.PhotoImage(file = "Untitled.png"))

	if "g" in pressed_keys:
		sprite.change_image(tk.PhotoImage(file = "sprites/2.png"))

	if "v" in pressed_keys:
		sprite.change_image(clear_img)

for i in range(1000):
	spr = Sprite("sprites/4.png", updateFunc=move)
	a.add_sprite(spr)

while 1:
	startTime = time()
	a.advance_frame()
	check_keys()
	endTime = time()
	print(pressed_keys)
	elapsedTime = endTime - startTime
	#print(1./elapsedTime)
	