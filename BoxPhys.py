physics_objects = []
colliders = []

# depth of area on the edges the box collier in which the objects are displaced
COLLIDER_ACTIVE_BOUNDARY = 100

class PhysicsObject():
	x = 0
	y = 0
	vel = [0,0]
	gravity = 0.3
	friction = 0.1
	colliders = {}
	type = "default"

	def __init__(self, type:str="default", colliders:dict={}, x:float=0, y:float=0, vel:list=[0,0], gravity:float=-0.3, friction:float=0.1):
		global physics_objects

		if type not in ["default", "immovable"]:
			type = 'default'

		self.type = type
		self.colliders = colliders
		self.x = x
		self.y = y
		self.vel = vel
		self.gravity = gravity
		self.friction = friction

		physics_objects.append(self)

	def advance_simulation(self):

		if self.type != "immovable":
			self.vel[1]-=self.gravity
			self.move(self.vel[0],self.vel[1])

		collision_checked = False

	def move(self, x:int, y:int):

		if self.type != "immovable":
			self.x += x
			self.y += y

	def add_vel(self, x:int, y:int):

		if self.type != "immovable":
			self.vel[0] += x
			self.vel[1] += y


	def delete_self(self):
		for collier in list(self.colliders.values()):
			collier.delete_self()

		physics_objects.remove(self)

	# default, meant to be extended
	def handle_trigger(self, collided_obj, my_collider, other_collider):
		pass

	def get_collision_displacement(self, collided_obj, my_collider, other_collider):
		global COLLIDER_ACTIVE_BOUNDARY
		
		top_dist = my_collider.bottom_edge()-other_collider.top_edge()
		bottom_dist = other_collider.bottom_edge() - my_collider.top_edge()
		right_dist = my_collider.right_edge() - other_collider.left_edge()
		left_dist = other_collider.right_edge() - my_collider.left_edge()

		
		if right_dist < COLLIDER_ACTIVE_BOUNDARY and right_dist > 0 and right_dist < top_dist and right_dist < bottom_dist:
			return [-right_dist, 0]

		elif left_dist < COLLIDER_ACTIVE_BOUNDARY and left_dist > 0 and left_dist < top_dist and left_dist < bottom_dist:
			return [left_dist, 0]

		elif top_dist < COLLIDER_ACTIVE_BOUNDARY and top_dist > 0:
			return [0, -top_dist]

		elif bottom_dist < COLLIDER_ACTIVE_BOUNDARY and bottom_dist > 0:
			return [0, bottom_dist]


		return [0,0]

	def handle_collision(self, collided_obj, my_collider, other_collider):

		if my_collider.type == 'trigger':
			self.handle_trigger(collided_obj, my_collider, other_collider)
			return

		if other_collider.type == 'trigger':
			collided_obj.handle_trigger(self, other_collider, my_collider)
			return

		displacement = self.get_collision_displacement(collided_obj, my_collider, other_collider)

		# nullify velocities in the direction of collision
		if displacement[0]!=0:
			collided_obj.vel[0] = 0
			self.vel[0] = 0
		elif displacement[1]!=0:
			collided_obj.vel[1]=0
			self.vel[1] = 0


		# can't do anything in this case. Shouldn't even happen tbh
		if collided_obj.type == "immovable" and self.type == "immovable":
			return

		# don't collide with self. allows overlapping hitboxes
		elif collided_obj == self:
			return

		# move the other obj outside of yourself
		elif collided_obj.type == "default" and self.type == "immovable":
			collided_obj.move(-displacement[0], -displacement[1])

		# move yourself outside of the other obj
		elif collided_obj.type == "immovable" and self.type == "default":
			self.move(displacement[0], displacement[1])

		# two default type objects, move the same distance
		else:
			self.move(displacement[0]/2, displacement[1]/2)
			collided_obj.move(-displacement[0]/2, -displacement[1]/2)


class Collider(object):
	
	x = 0
	y = 0
	width = 0
	height = 0
	id = "default"
	type = "rigid"
	parent = None
	
	def __init__(self, x:float, y:float, parent:PhysicsObject, width:float, height:float, id:str="default", type:str="rigid"):
		global colliders
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.id = id
		self.type = type
		self.parent = parent

		colliders.append(self)

	def delete_self(self):
		self.parent.colliders.pop(self.id)
		colliders.remove(self)

	# helper functions for edges of the collider
	def left_edge(self):
		return self.x+self.parent.x

	def right_edge(self):
		return self.x+self.width+self.parent.x
	
	def bottom_edge(self):
		return self.y+self.height+self.parent.y

	def top_edge(self):
		return self.y+self.parent.y

	# helper functions to get locations of all points
	def NW(self):
		return [self.x+self.parent.x, self.y+self.parent.y]

	def NE(self):
		return [self.x+self.width+self.parent.x, self.y+self.parent.y]

	def SW(self):
		return [self.x+self.parent.x, self.y+self.height+self.parent.y]

	def SE(self):
		return [self.x+self.width+self.parent.x, self.y+self.height+self.parent.y]



def _colliders_intersect(A:Collider, B:Collider):
	#check if starting point of one rectangle is within projection another on x
	A_SW, A_NE = A.SW(), A.NE()
	B_SW, B_NE = B.SW(), B.NE()
	if (A_SW[0]>=B_NE[0] or A_NE[0]<=B_SW[0] or A_SW[1]<=B_NE[1] or A_NE[1]>=B_SW[1]):
		return False
	else:
		return True

def _handle_all_collisions(arr:list):

	#compare every element in rect list to every next element
	#which gives us total of (n-1)^2 / 2 number of comparisons
	for i in range(len(arr)):
		for j in range(i + 1, len(arr)):
			if _colliders_intersect(arr[i], arr[j]):
				arr[i].parent.handle_collision(arr[j].parent, arr[i], arr[j])

def advance_phys_simulation():
	for obj in physics_objects:
		obj.advance_simulation()

	_handle_all_collisions(colliders)

