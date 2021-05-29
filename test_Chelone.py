from BoxPhys import *
from Chelone import *
from time import *
import unittest

chelone = init()

class TestSpriteLoader(unittest.TestCase):
	
	def setUp(self):
		self.spriteloader = SpriteLoader(sprite_dir = "")
	
	def test_load_anim(self):
		self.assertEqual(self.spriteloader.load_anim("./tests/test.anim"), 
			["./tests/1.png", None, "./tests/2.png"])
	
	def test_load(self):
		results = self.spriteloader.load("./tests/tmp.png")
		
		isTrue = isinstance(results, SpriteLoader.SpriteFrame)
		isTrue = isTrue and results.extra == {"offset":{"x": 100, "y": 100}}
		isTrue = isTrue and results.hitboxes == {"body":{"x":0,"y":0,"width":100,"height":100,"type":"rigid"}}
		isTrue = isTrue and results.image != None
		isTrue = isTrue and results.parent is self.spriteloader
		isTrue = isTrue and results.path == "./tests/tmp.png"
		
		self.assertTrue(isTrue, "Sprite loading failed")
	
	def test_create_colliders(self):
		self.sprite = Sprite("2", self.spriteloader.load("./tests/1.png"))
		secondImage = self.spriteloader.load("./tests/tmp.png")
		self.sprite.frame = secondImage
		self.spriteloader.create_colliders(self.sprite)
		expectedHitbox = {"x":0,"y":0,"width":100,"height":100,"type":"rigid"}
		
		isTrue = expectedHitbox["x"] == self.sprite.colliders["body"].x
		isTrue = isTrue and expectedHitbox["y"] == self.sprite.colliders["body"].y
		isTrue = isTrue and expectedHitbox["width"] == self.sprite.colliders["body"].width
		isTrue = isTrue and expectedHitbox["height"] == self.sprite.colliders["body"].height
		isTrue = isTrue and expectedHitbox["type"] == self.sprite.colliders["body"].type
		
		self.assertTrue(isTrue, "Sprite collider update frame")



class TestAnimStateSystem(unittest.TestCase):

	def setUp(self):
		self.animstate = AnimStateSystem(state_anim_directory = "")

	def test_flip(self):
		self.animstate.flip()
		self.assertEqual(self.animstate.orientation, "left")

	# def test_update_state(self):
	# 	isBool = False
	# 	self.animstate._update_state()
	# 	assertTrue(isBool, "Your function is incorrect")	

class TestSprite(unittest.TestCase):

	def setUp(self):
		self.spriteloader = SpriteLoader("")
		self.sprite = Sprite("2", self.spriteloader.load("./tests/1.png"))
		sleep(1)

	def test_delete_self(self):
		self.sprite.delete_self()
		chelone.advance_frame()
		isTrue = self.sprite not in physics_objects
		isTrue = isTrue and self.sprite.colliders == {}
		isTrue = isTrue and self.sprite.id not in chelone._sprites[25].keys()
		self.assertTrue(isTrue, "Sprite remove unsuccesful")

	def test_update_all(self):
		
