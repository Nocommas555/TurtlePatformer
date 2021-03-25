from Chelone import *

# setting up a basic scene to test
Chelone = init(1620,800)

loader = SpriteLoader()

class Player(Sprite):
	flag = False
	last_x = 0

	def move(self, x, y):
		super().move(x, y)
		Chelone.move_camera(x,0)

	def setup(self):
		print("setup Player")
		self.flag = False
		self.last_x = 0

	def update(sprite):
		global Chelone

		if 'w' in Chelone.pressed_keys and not sprite.flag:
			sprite.add_vel(0,-10)
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
			Chelone.move_camera(3,0)

		if "e" in Chelone.pressed_keys:
			sprite.change_image(loader.load("Untitled.png"))

		if "g" in Chelone.pressed_keys:
			sprite.change_image(loader.load("stick_figure/2.png"))

		sprite.last_x = sprite.x

	def handle_collision(self, collided_obj, my_collider, other_collider):
		if my_collider.id == "1":
			super().handle_collision(collided_obj, my_collider, other_collider)
			return


		
#for i in range(1):
spr = Player(loader.load("tmp.png"), gravity=-0.3, x = 100)
Chelone.add_sprite(spr)

ground = Sprite(loader.load("gnd.png"),phys_type="immovable", x=0, y=350)
Chelone.add_sprite(ground)

block = Sprite(loader.load("tmp.png"), phys_type="immovable", x=500, y=150)
Chelone.add_sprite(block, 49)

movable = Sprite(loader.load("tmp.png"), x=150, y=200)
Chelone.add_sprite(movable, 49)


while 1:
	startTime = time()
	Chelone.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime
	print(1/elapsedTime)