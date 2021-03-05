from Chelone import *

# setting up a basic scene to test
a = init(1000,500)

loader = SpriteLoader()
a.add_sprite(Sprite(loader.load("Untitled.png"),10,10),40)


class Player(Sprite):
	
	def setup(self):
		print("setup Player")

	def update(sprite):

		if 'w' in pressed_keys:
			sprite.move(0,-1)
		if 'a' in pressed_keys:
			sprite.move(-1,0)
		if 's' in pressed_keys:
			sprite.move(0,1)
		if 'd' in pressed_keys:
			sprite.move(1,0)

		if "q" in pressed_keys:
			sprite.shedule_anim(loader.load("stick_figure"))
			flag = False

		if "e" in pressed_keys:
			sprite.change_image(loader.load("Untitled.png"))

		if "g" in pressed_keys:
			sprite.change_image(loader.load("stick_figure/2.png"))

		if "v" in pressed_keys:
			sprite.change_image(clear_img)

for i in range(1000):
	spr = Player(loader.load("test.gif"))
	a.add_sprite(spr)



while 1:
	startTime = time()
	a.advance_frame()
	endTime = time()
	elapsedTime = endTime - startTime
	print(1./elapsedTime)