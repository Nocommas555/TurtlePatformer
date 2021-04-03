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
import re

Chelone = None


def init(resolution_x:int, resolution_y:int):
	global Chelone, _root, _canvas
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
	if event.keysym not in Chelone.caught_keys:
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
		hitboxes = {}
		extra = {}
		image = None
		path = ""
		parent = None

		def __init__(self, file:str, parent, hitboxes:list = [], extra:dict = {}):
			self.image = tk.PhotoImage(file = file)
			self.hitboxes = hitboxes
			self.extra = extra
			self.path = file
			self.parent = parent


	def __init__(self, sprite_dir:str = "sprites/"):
		self._sprite_dir = sprite_dir
		self._storage = {}

	def load_anim(self, path:str):
		if os.path.exists(self._sprite_dir+path):
			return ["/".join(path.split("/")[:-1])+"/"+x if x!="None" else None for x in json.load(open(self._sprite_dir+path))]

		else:
			print("wrong anim path")
			return [None]

	def load(self, path:str):

		path = self._sprite_dir + path

		# check if we already loaded the image
		if path in self._storage.keys():
			return self._storage[path]

		parent_path = "/".join(path.split("/")[:-1])
		file = path.split("/")[-1]

		if os.path.exists(path) and os.path.exists(parent_path+'/'+"img_descr.json"):
			
			img_descr = json.load(open(parent_path+'/'+"img_descr.json"))["images"][file]
		
			if os.path.isfile(path):

				hitboxes = {}
				if "hitboxes" in img_descr:
					hitboxes = img_descr["hitboxes"]

				extra = {}
				if "extra" in img_descr:
					extra = img_descr["extra"]

				self._storage[path] = self.SpriteFrame(path, self, hitboxes, extra)

				if "scale" in img_descr:
					self._storage[path].image = self._storage[path].image.zoom(img_descr["scale"])
				
				return self._storage[path]

			else:
				return self._load_anim(path)

	def create_colliders(self, sprite):
		
		for key in sprite.frame.hitboxes.keys():
			hitbox = sprite.frame.hitboxes[key]

			if hitbox == "remove":
				sprite.colliders[key].delete_self()
				
			else:
				if key in sprite.colliders:
					sprite.colliders[key].delete_self()
					
				sprite.colliders[key] = Collider(hitbox["x"], hitbox["y"],\
					sprite, hitbox["width"], hitbox["height"], key, hitbox["type"])

		return sprite.colliders
		
	def unload(self, path:str):
		self._storage.pop(path)

	def unload_all(self):

		for path in self._storage.keys():
			self.unload(path)

class AnimStateSystem():
	states = {}
	anim_state = "None"
	orientation = "right"
	state_anim_directory = ""
	_anim_frame = 0
	_anim = []
	"""interface for handling anim state changes and their functions"""
	def __init__(self, start_state:str = "None", state_anim_directory:str = ""):
		
		self.states["None"] = lambda: 0 # noop
		self.state_anim_directory = state_anim_directory
		self.update_anim_state(self.anim_state)
		self._anim_frame = 0
		self._anim = []

	def flip(self):
		if self.anim_state != "None":
			self.start_anim(self.state_anim_directory + "/" + self.anim_state + "_" + self.orientation + ".anim", self._anim_frame)

		if self.orientation == "left":
			self.orientation = "right"
		else:
			self.orientation = "left"


	def _update_state(self):
		self.states[self.anim_state]()

	def update_anim_state(self, state):
		self.anim_state = state
		if state != "None":
			self.start_anim(self.state_anim_directory + "/" + state + "_" + self.orientation + ".anim")

	def start_anim(self, anim_frames:Union[str, list], start_frame:int):
		pass

class Sprite(PhysicsObject, AnimStateSystem):
	"""Object that contains data about the sprite. Also can be used to have code ran on each frame"""
	x = 0
	y = 0
	frame = None
	image_tk = None
	parent_canvas = None
	_anim = []
	_anim_frame = 0
	id = ""
	_current_offset = {"x":0,"y":0}

	# updateFunc is a function that takes self and gets called every frame
	# setupFunc is a function that takes self and gets called once, at setup

	def __init__(self, id:str, frame:SpriteLoader.SpriteFrame, x:int = 0, y:int = 0, phys_type:str="default", gravity:float=-0.3, friction:float=0.1, layer = 25, state_anim_directory:str=".", **kargs):
		
		PhysicsObject.__init__(self,phys_type,{},x,y,[0,0],gravity,friction)

		self.layer = 25
		self.id = Chelone.get_unique_id(id)  
		self.frame = frame
		self.image_tk = None
		self.parent_canvas = None	
		frame.parent.create_colliders(self)
		Chelone.add_sprite(self, layer)

		self.setup(kargs)
		
		# because setup should define anim states, we should setup AnimStateSystem 
		AnimStateSystem.__init__(self, state_anim_directory = state_anim_directory)

		self._anim = [frame]
		self._anim_frame = 0	

	# made to be extended
	def setup(self, kargs):
		pass

	# made to be extended
	def update(self):
		pass

	def delete_self(self):
		PhysicsObject.delete_self(self)
		self.parent_canvas.delete(self.image_tk)

		if self.id in Chelone._sprites[self.layer]:
			Chelone._sprites[self.layer].pop(self.id)

	def _update(self):
		self.update()
		self.advance_anim()
		self._update_state()	

	def move(self, x:int, y:int):
		self.x += x
		self.y += y
		self.parent_canvas.move(self.image_tk, x, y)

	def change_image(self, frame:SpriteLoader.SpriteFrame, stop_anim:bool = True):

		if self._current_offset["x"]!=0 or self._current_offset["y"]!=0:
			self.parent_canvas.move(self.image_tk,self._current_offset["x"], self._current_offset["y"])
			self._current_offset["x"] = 0
			self._current_offset["y"] = 0


		self.frame = frame
		self.parent_canvas.itemconfig(self.image_tk, image = frame.image)
		self.frame.parent.create_colliders(self)

		if stop_anim:
			self._anim = [frame]
			self._anim_frame = 0
			self.update_anim_state("None")

		if "offset" in self.frame.extra.keys():
			self.parent_canvas.move(self.image_tk,-self.frame.extra["offset"]["x"], -self.frame.extra["offset"]["y"])
			self._current_offset["x"] = self.frame.extra["offset"]["x"]
			self._current_offset["y"] = self.frame.extra["offset"]["y"]


	def start_anim(self, anim_frames:Union[str,list], start:int = 0):
		global clear_img
		
		if isinstance(anim_frames, str):
			anim_frames = self.frame.parent.load_anim(anim_frames)

		self._current_offset["x"] = 0
		self._current_offset["y"] = 0
		self.parent_canvas.delete(self.image_tk)
		self.image_tk = self.parent_canvas.create_image(self.x-Chelone.camera.x, self.y-Chelone.camera.y, anchor = tk.NW, image = self.frame.image)
		self._anim = anim_frames
		self._anim_frame = start

	def advance_anim(self):
		if len(self._anim)>1:

			# loop animation automatically
			if (self._anim_frame >= len(self._anim)):
				self._anim_frame = 0

			if self._anim[self._anim_frame] != None:
				self.change_image(self.frame.parent.load(self._anim[self._anim_frame]), stop_anim = False)

			self._anim_frame += 1		


class SpriteRenderer():
	"""Main drawing class. Handles every sprite"""
	root = None
	screen = None
	_sprites = []
	_prev_draw_time = None
	_ids = {}

	caught_keys_prev = []
	caught_keys = []
	pressed_keys = []

	TARGET_FPS = 60
	camera = None

	class Camera(object):
		"""data associated with the camera"""
		def __init__(self, screen, x=0, y=0):
			self.x = 0
			self.y = 0
			self.screen = screen

		def move(self, x, y):
			self.x += x
			self.y += -y
			self.screen.move("all", -x, y)
			

	def __init__(self, root: tk.Tk, screen:tk.Canvas):
		self.root = root
		self.screen = screen
		self.camera = self.Camera(screen)

		# 50 different z layers
		self._sprites = []
		for i in range(50):
			self._sprites.append({})

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
			for sprite in layer.values():
				sprite._update()


		advance_phys_simulation()

		self.root.update()
		self.next_frame += self.frame_period

		check_keys()
	
	def get_unique_id(self, id:str):
		if id not in self._ids:
			self._ids[id] = 1
		else:
			self._ids[id] += 1

		return id + "_" + str(self._ids[id])

	def relayer(self):
		for layer in self._sprites[::-1]:
			for spr in layer.values():
				self.screen.tag_raise(spr.image_tk)

	def add_sprite(self, sprite:Sprite, layer:int = 25):
		
		if layer < 1 or layer > 49:
			return

		sprite.layer = layer
		self._sprites[layer][sprite.id]=sprite

		if sprite.image_tk == None:
			sprite.image_tk = self.screen.create_image(sprite.x-self.camera.x, sprite.y-self.camera.y, anchor = tk.NW, image = sprite.frame.image)
		
		sprite.parent_canvas = self.screen
		self.relayer()


	def bind(func:Callable, key:str):
		self.root.bind(func, key)


	