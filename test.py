from Chelone import *

# setting up a basic scene to test
Chelone = init(1000,500)

loader = SpriteLoader()
Chelone.add_sprite(Sprite(loader.load("Untitled.png"),10,10),40)


class Player(Sprite):
	
	def setup(self):
		print("setup Player")

	def update(sprite):
		global Chelone

		if 'w' in Chelone.pressed_keys:
			sprite.move(0,-1)
		if 'a' in Chelone.pressed_keys:
			sprite.move(-1,0)
		if 's' in Chelone.pressed_keys:
			sprite.move(0,1)
		if 'd' in Chelone.pressed_keys:
			sprite.move(1,0)

		if "q" in Chelone.pressed_keys:
			sprite.shedule_anim(loader.load("stick_figure"))
			flag = False

		if "e" in Chelone.pressed_keys:
			sprite.change_image(loader.load("Untitled.png"))

		if "g" in Chelone.pressed_keys:
			sprite.change_image(loader.load("stick_figure/2.png"))

		if "v" in Chelone.pressed_keys:
			sprite.change_image(clear_img)

for i in range(1000):
	spr = Player(loader.load("test.gif"))
	Chelone.add_sprite(spr)



while 1:
	startTime = time()
	Chelone.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime

	#print(Chelone.pressed_keys)