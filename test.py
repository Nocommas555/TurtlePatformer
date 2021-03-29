from Chelone import *

# setting up a basic scene to test
Chelone = init(1620,800)

loader = SpriteLoader()

class Player(Sprite):
	flag = False
	last_x = 0

	def move(self, x, y):
		super().move(x, y)
		Chelone.camera.move(x,0)

	def setup(self, kargs):
		print("setup Player")
		self.flag = False
		self.last_x = 0
		
	def update(sprite):

		if 'w' in Chelone.pressed_keys and not sprite.flag:
			sprite.add_vel(0,-23)
			sprite.flag = True

		if 'a' in Chelone.pressed_keys:
			sprite.move(-3,0)

		if 's' in Chelone.pressed_keys:
			sprite.move(0,10)
		if 'd' in Chelone.pressed_keys:
			sprite.move(3,0)

			

		if sprite.flag and 'w' not in Chelone.pressed_keys:
			sprite.flag = False

		if "q" in Chelone.pressed_keys:
			Chelone.camera.move(-3,3)

		if "e" in Chelone.pressed_keys:
			Chelone.camera.move(3,-3)

		if "g" in Chelone.pressed_keys:
			sprite.start_anim(loader.load_anim("anakin/idle.anim"))

		sprite.last_x = sprite.x

	def handle_collision(self, collided_obj, my_collider, other_collider):
		if my_collider.id == "1":
			super().handle_collision(collided_obj, my_collider, other_collider)
			return

	def delete_self(self):
		print("game_over")
		saved_sprites = Chelone._sprites
		Chelone._sprites = [{},{}]
		game_over = Sprite("game_over", loader.load("game_over.png"), x=450+Chelone.camera.x, phys_type = "immovable")
		Chelone.add_sprite(game_over,1)
		saved_sprites[1][game_over.id]=game_over
		super().delete_self()

		# loop while dead
		while "Return" not in Chelone.pressed_keys:
			Chelone.advance_frame()

		Chelone._sprites = saved_sprites
		player = Player("Player", self.frame, x = self.x, y = self.y, gravity = self.gravity)
		
		Chelone.add_sprite(player)
		Chelone.remove_sprite(game_over.id)
		

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
	def update(sprite):
		global Chelone

		if sprite.counter < 300 and sprite.moving == True:
			sprite.move(-sprite.velocity, 0)
		elif sprite.moving == True:
			if sprite.counter >= 600:
				sprite.counter = 0
			else:	
				sprite.move(sprite.velocity, 0)


		sprite.counter += 1	
		
		sprite.shoot_counter = max(0,sprite.shoot_counter-1)

		if sprite.player_seen == False and sprite.shoot_counter == 0:
			sprite.moving = True

		sprite.player_seen = False

	def handle_trigger(sprite, collided_obj, my_collider, other_collider):
		if type(collided_obj) == Player:
			if sprite.shoot_counter==0:
				sprite.moving = False
				if my_collider.id == "2":
					laser = Laser("Laser", loader.load("laser.png"),x=sprite.x - 70, y = sprite.y+50, velocity = [-2, 0])			
					Chelone.add_sprite(laser)
				elif my_collider.id == "3":	
					laser = Laser("Laser", loader.load("laser.png"),x=sprite.x + 100, y = sprite.y+50, velocity = [2, 0])			
					Chelone.add_sprite(laser)
				sprite.shoot_counter = sprite.SHOOT_CD

class Laser(Sprite):
	def setup(self, kargs):
		if "velocity" not in kargs.keys():
			self.velocity = [-1, 0]
		else:
			self.velocity = kargs["velocity"]

		self.gravity = 0
		

	def update(this):
		this.move(this.velocity[0], this.velocity[1])

	def handle_trigger(self, collided_obj, my_collider, other_collider):
		Chelone.remove_sprite(collided_obj.id)
		Chelone.remove_sprite(self.id)
		print("Laser attacked " + collided_obj.id)

spr = Player("Player",loader.load("tmp.png"), gravity=-1, x = 100)
Chelone.add_sprite(spr, 10)

drd1 = Droid_1("Droid",loader.load("droid.png"), x = 1000)
Chelone.add_sprite(drd1)

#drd2 = Droid_1("Droid 2",loader.load("droid.png"), x = 1200)
#Chelone.add_sprite(drd2)

#drd3 = Droid_1("Droid 3",loader.load("droid.png"), x = 1400)
#Chelone.add_sprite(drd3)

ground = Sprite("Ground",loader.load("gnd.png"),phys_type="immovable", x=0, y=650)
Chelone.add_sprite(ground, 49)

block = Sprite("Block",loader.load("tmp.png"), phys_type="immovable", x=500, y=150)
Chelone.add_sprite(block, 30)

movable = Sprite("Movable",loader.load("tmp.png"), x=150, y=200)
Chelone.add_sprite(movable, 30)

#laser = Laser("Laser",loader.load("laser.png"), x = 900)
#Chelone.add_sprite(laser)

Chelone.camera.move(-300,0)
print(Chelone.get_unique_id("Player"))

while 1:
	startTime = time()
	Chelone.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime