'''
Chelone is a graphics library created specifically for our platformer
It is a wrapper over the included tkinter library that seeks to become an
alternative to pyGame with more of a focus on sprites rather then  primitives

The engine includes basic loading, collision detection, animation, drawing, z-layering and complex backrounds
'''
from BoxPhys import *
import tkinter as tk
from typing import Union, Callable
from time import time, sleep
import os
import json


Chelone = None

def init(resolution_x:int, resolution_y:int):
	global Chelone
	# Create the window with the Tk class
	root = tk.Tk()
	
	root.bind("<Key>", on_key_press)
	root.bind("<KeyRelease>", on_key_release)
	root.bind("<FocusOut>", FocusOut)
	# Create the canvas and make it visible with pack()
	canvas = tk.Canvas(root, width = resolution_x, height = resolution_y)
	canvas.pack() # this makes it visible

	Chelone = SpriteRenderer(root, canvas)
	return Chelone


def FocusOut(event):
	Chelone.caught_keys_prev = []
	Chelone.caught_keys = []
	Chelone.pressed_keys = []

def check_keys():

	# remove keys not caught for 2 frames
	for key in Chelone.pressed_keys:
		if key not in Chelone.caught_keys and\
		  key not in Chelone.caught_keys_prev:

			Chelone.pressed_keys.remove(key)

	for key in Chelone.caught_keys:
		if key not in Chelone.pressed_keys:
			Chelone.pressed_keys.append(key)

	Chelone.caught_keys_prev = Chelone.caught_keys.copy()


def on_key_press(event):
	Chelone.caught_keys.append(event.keysym)


def on_key_release(event):
	Chelone.caught_keys.remove(event.keysym)

"""Handles loading sprites and animations"""
"""There can be multiple instances at the same time"""
class SpriteLoader():
	_sprite_dir = "sprites/"
	_storage = {}

	class SpriteFrame():
		"""A frame of animation that has extra data for collision detection"""
		hitboxes = []
		extra = {}
		image = None
		path = ""
		parent = None

		def __init__(self, file:str, parent, hitboxes:list = [], extra:dict = {}):
			self.image = tk.PhotoImage(file = file)
			self.hitboxes = []
			self.extra = {}
			self.path = file
			self.parent = parent


	def __init__(self, sprite_dir:str = "sprites/"):
		self._sprite_dir = sprite_dir
		self._storage = {}

	def _load_anim(self, path:str):
		if not os.path.exists(path + "/anim_descr.json"):
			print("animation does not exist!")
			return

		anim_descr = json.load(open(path + "/anim_descr.json", "r"))
		self._storage[path] = []

		for frame in anim_descr["frames"]:
			
			if "hitboxes" not in frame.keys():
				frame["hitboxes"] = []

			if "extra" not in frame.keys():
				frame["extra"] = {}

			if frame["image"] != "None":
				self._storage[path].append(self.SpriteFrame(path + '/' + frame["image"], self, frame["hitboxes"], frame["extra"]))

			else:
				self._storage[path].append(None)

		return(self._storage[path])

	def load(self, path:str):

		path = self._sprite_dir + path
		
		# check if we already loaded the image/anim
		if path in self._storage.keys():
			return self._storage[path]

		if os.path.exists(path):

			if os.path.isfile(path):
				self._storage[path] = self.SpriteFrame(path, self)
				return self._storage[path]

			else:
				return self._load_anim(path)

		else:
			print("the path is invalid, loading failed for " + path)

	def create_colliders(self, sprite:Sprite, path:str = None):
		if path == None:
			path = sprite.frame.path

		if path not in self._storage.keys():
			self.load(path)
		self._storage[path]

		for key in self._storage[path]["hitboxes"].keys():
			hitbox = self._storage[path]["hitboxes"][key]
			sprite.colliders[key] = Collider(hitbox["x"], hitbox["y"],\
				sprite, hitbox["width"], hitbox["height"], key, hitbox["type"])

		return sprite.colliders
		
	def unload(self, path:str):
		self._storage.pop(path)

	def unload_all(self):

		for path in self._storage.keys():
			self.unload(path)

class Sprite(PhysicsObject):
	"""Object that contains data about the sprite. Also can be used to have code ran on each frame"""
	x = 0
	y = 0
	frame = None
	image_tk = None
	parent_canvas = None
	_anim = []
	_anim_frame = 0
	
	# updateFunc is a function that takes self and gets called every frame
	# setupFunc is a function that takes self and gets called once, at setup

	def __init__(self, frame:SpriteLoader.SpriteFrame, x:int = 0, y:int = 0, phys_type:str="default", gravity:float=-0.3, friction:float=0.1):
		super().__init__(phys_type,{},x,y,[0,0],gravity,friction)
		self.x = x
		self.y = y
		self.frame = frame
		self.image_tk = None
		self.parent_canvas = None
		self._anim = [frame]
		self._anim_frame = 0
		
		self.setup()

	# made to be extended
	def setup(self):
		pass

	# made to be extended
	def update(self):
		pass


	def _update(self):
		self.update()
		self.advance_anim()		

	def move(self, x:int, y:int):
		self.x += x
		self.y += y
		self.parent_canvas.move(self.image_tk, x, y)

	def change_image(self, frame:SpriteLoader.SpriteFrame, stop_anim:bool = True):

		if stop_anim and len(self._anim)>1:
			self._anim = [frame]

		self.frame = frame
		self.parent_canvas.itemconfig(self.image_tk, image = frame.image)

	def advance_anim(self):

		if len(self._anim)>1:

			# loop animation automatically
			if (self._anim_frame >= len(self._anim)):
				self._anim_frame = 0

			if self._anim[self._anim_frame] != None:
				self.change_image(self._anim[self._anim_frame], stop_anim = False)

			self._anim_frame += 1
		

	def shedule_anim(self, anim_frames:list, start:int = 0):
		global clear_img

		self._anim = anim_frames
		self._anim_frame = start

class SpriteRenderer():
	"""Main drawing class. Handles every sprite"""
	root = None
	screen = None
	_sprites = []
	_prev_draw_time = None

	caught_keys_prev = []
	caught_keys = []
	pressed_keys = []

	TARGET_FPS = 60

	def __init__(self, root: tk.Tk, screen:tk.Canvas):
		self.root = root
		self.screen = screen
		
		# 50 different z layers
		self._sprites = []
		for i in range(50):
			self._sprites.append([])

	def draw_gui(self):
		pass


	frame_period = 1.0/TARGET_FPS
	now = time()
	next_frame = now + frame_period

	def advance_frame(self):

		while self.now < self.next_frame:
			sleep(self.next_frame - self.now)
			self.now = time()

		for layer in self._sprites:
			for sprite in layer:
				sprite._update()


		advance_phys_simulation()

		self.root.update()
		self.next_frame += self.frame_period

		check_keys()

	def move_camera(self, x, y):
		self.screen.move("all", x, y)

	def add_sprite(self, sprite:Sprite, layer:int = 25):
		
		#layer 0 reserved for gui, layer 50 onward does not exist
		if layer < 1 or layer > 49:
			return

		self._sprites[layer].append(sprite)

		sprite.image_tk = self.screen.create_image(sprite.x, sprite.y, anchor = tk.NW, image = sprite.frame.image)
		sprite.parent_canvas = self.screen

		for i, z_layer in enumerate(self._sprites):
			if len(z_layer) > 0 and i <= layer:
				self.screen.tag_raise(sprite.image_tk, z_layer[0].image_tk)

	def bind(func:Callable, key:str):
		self.root.bind(func, key)


	