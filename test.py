from Chelone import *

# setting up a basic scene to test
Chelone = init(1000,500)

loader = SpriteLoader()
Chelone.add_sprite(Sprite(loader.load("Untitled.png"),10,10),40)


class Player(Sprite):
	flag = False

	def setup(self):
		print("setup Player")
		self.flag = False

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
			sprite.shedule_anim(loader.load("stick_figure"))

		if "e" in Chelone.pressed_keys:
			sprite.change_image(loader.load("Untitled.png"))

		if "g" in Chelone.pressed_keys:
			sprite.change_image(loader.load("stick_figure/2.png"))

for i in range(1):
	spr = Player(loader.load("tmp.png"), gravity=-0.3)
	Chelone.add_sprite(spr)

spr.colliders["1"] = Collider(0,0,spr,100,100,"1","rigid")

ground = Sprite(loader.load("gnd.png"),phys_type="immovable", x=0, y=400)
Chelone.add_sprite(ground)
ground.colliders["1"] = Collider(0,0,ground,1000,1000,"1","rigid")

block = Sprite(loader.load("tmp.png"), phys_type="immovable", x=500, y=200)
Chelone.add_sprite(block, 49)
block.colliders["1"] = Collider(0,0,block,100,100,"2","rigid")

while 1:
	startTime = time()
	Chelone.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime
	print(block.colliders["1"].NW(), spr.colliders['1'].NW())
	#print(1/elapsedTime)