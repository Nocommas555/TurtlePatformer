from Chelone import *
from time import time
# setting up a basic scene to test
Chelone = init(1600,800)

loader = SpriteLoader()

class Player(Sprite):
	grounded = False
	w_pressed = False
	camera_lagbehind = [0.01, 0.125]
	camera_offset = [600, 300]

	def setup(self, kargs):
		print("setup Player")
		self.grounded = False
		self.w_pressed = False
		self.anim_state = "idle"
		self.start_anim(loader.load_anim("anakin/idle.anim"))

		if "camera_lagbehind" in kargs:
			self.camera_lagbehind = kargs["camera_lagbehind"]
		else:
			self.camera_lagbehind = [0.05, 0.125]


		if "camera_offset" in kargs:
			self.camera_offset = kargs["camera_offset"]
		else:
			self.camera_offset = [600, 300]

	def update(self):

		if 'w' in Chelone.pressed_keys and self.grounded and not self.w_pressed:
			self.add_vel(0,-23)

		if 'a' in Chelone.pressed_keys:
			self.move(-5,0)
			if self.anim_state != "run_left":
				self.anim_state = "run_left"
				if self.anim_state == "run_right":
					self.start_anim(loader.load_anim("anakin/run_left.anim"), self._anim_frame)
				else:
					self.start_anim(loader.load_anim("anakin/run_left.anim"))

		elif 'd' in Chelone.pressed_keys:
			self.move(5,0)
			if self.anim_state != "run_right":
				self.anim_state = "run_right"
				if self.anim_state == "run_left":
					self.start_anim(loader.load_anim("anakin/run_right.anim"), self._anim_frame)
				else:
					self.start_anim(loader.load_anim("anakin/run_right.anim"))
		else:
			if self.anim_state != "idle":
				self.anim_state = "idle"
				self.start_anim(loader.load_anim("anakin/idle.anim"))

		# smooth camera follow
		Chelone.camera.move(-self.camera_lagbehind[0]*(Chelone.camera.x-self.x+self.camera_offset[0]), self.camera_lagbehind[1]*(Chelone.camera.y-self.y+self.camera_offset[1]))


		self.grounded = False
		self.w_pressed = 'w' in Chelone.pressed_keys

	def handle_collision(self, collided_obj, my_collider, other_collider, handled=False):
		

		displacement = self.get_collision_displacement(collided_obj, my_collider, other_collider)
		super().handle_collision(collided_obj,my_collider,other_collider,handled)
		
		print(displacement)
		if displacement[1]<0 and not self.vel[1]<0 and my_collider.type!="trigger" and other_collider.type != "trigger":
			self.grounded=True


	def delete_self(self):
		print("game_over")
		saved_sprites = Chelone._sprites
		Chelone._sprites = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
		game_over = Sprite("game_over", loader.load("game_over.png"), x=450+Chelone.camera.x, phys_type = "immovable", layer = 1)
		Chelone.add_sprite(game_over,1)
		saved_sprites[1][game_over.id]=game_over


		# loop while dead
		while "Return" not in Chelone.pressed_keys:
			check_keys()
			Chelone.root.update()

		Chelone.next_frame = time()
		Chelone.now = time()
		Chelone._sprites = saved_sprites
		super().delete_self()
		player = Player("Player", loader.load("tmp.png"), x = 250, y = 0, gravity = self.gravity)
		Chelone.camera.move(-Chelone.camera.x - 300, 0)
		Chelone.add_sprite(player)
		game_over.delete_self()
		

class Droid_1(Sprite):
	def setup(self, kargs):
		self.counter = 0
		self.counter2 = 0
		self.velocity = 1
		self.delete = False
		self.moving = True
		self.SHOOT_CD = 240
		self.shoot_counter=0
		self.player_seen = False
	
	def update(self):
		global Chelone

		if self.counter < 300 and self.moving == True:
			self.move(-self.velocity, 0)
		elif self.moving == True:
			if self.counter >= 600:
				self.counter = 0
			else:	
				self.move(self.velocity, 0)


		self.counter += 1	
		
		self.shoot_counter = max(0,self.shoot_counter-1)

		if self.player_seen == False and self.shoot_counter == 0:
			self.moving = True

		self.player_seen = False

	def handle_trigger(self, collided_obj, my_collider, other_collider):
		if type(collided_obj) == Player:
			if self.shoot_counter==0:
				self.moving = False
				if my_collider.id == "2":
					laser = Laser("Laser", loader.load("laser.png"),x=self.x - 70, y = self.y+50, velocity = [-2, 0])			
				elif my_collider.id == "3":	
					laser = Laser("Laser", loader.load("laser.png"),x=self.x + 100, y = self.y+50, velocity = [2, 0])			
				self.shoot_counter = self.SHOOT_CD

class Laser(Sprite):
	def setup(self, kargs):
		if "velocity" not in kargs.keys():
			self.velocity = [-1, 0]
		else:
			self.velocity = kargs["velocity"]

		self.gravity = 0
		

	def update(self):
		self.move(self.velocity[0], self.velocity[1])

	def handle_trigger(self, collided_obj, my_collider, other_collider):
		if type(collided_obj) != Droid_1:
			self.delete_self()
			collided_obj.delete_self()
			print("Laser attacked " + collided_obj.id)

spr = Player("Player",loader.load("tmp.png"), gravity=-0.7, x = 100, layer = 10)

drd1 = Droid_1("Droid",loader.load("droid.png"), x = 1000)

#drd2 = Droid_1("Droid 2",loader.load("droid.png"), x = 1200)
#Chelone.add_sprite(drd2)

#drd3 = Droid_1("Droid 3",loader.load("droid.png"), x = 1400)
#Chelone.add_sprite(drd3)

ground = Sprite("Ground",loader.load("gnd.png"),phys_type="immovable", x=0, y=650, layer=49)

block = Sprite("Block",loader.load("tmp.png"), phys_type="immovable", x=500, y=350)

# movable = Sprite("Movable",loader.load("tmp.png"), x=150, y=200)
# Chelone.add_sprite(movable, 30)

#laser = Laser("Laser",loader.load("laser.png"), x = 900)
#Chelone.add_sprite(laser)

print(Chelone.get_unique_id("Player"))

while 1:
	startTime = time()
	Chelone.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime
	print(Chelone.camera.x, Chelone.camera.y)