'''
BoxPhys is an open-source lightweight 2d physics engine.
It has support for 2d box colliders, velocities, gravity and trigger hitboxes.
'''
physics_objects = []
colliders = []
_removing = []

# depth of area on the edges the box collier in which the objects are displaced
COLLIDER_ACTIVE_BOUNDARY = 100


class PhysicsObject():
    '''Basic class for all rigidbodies. handles movement and collision with other objects, '''
    x = 0
    y = 0
    vel = [0, 0]
    gravity = 0.3
    friction = 0.1
    colliders = {}
    type = "default"

    def __init__(self, type: str = "default", colliders: dict = None,
                 x: float = 0, y: float = 0,
                 vel: list = None,
                 gravity: float = -0.3, friction: float = 0.1):
        global physics_objects

        if type not in ["default", "immovable"]:
            type = 'default'

        if colliders is None:
            colliders = {}

        if vel is None:
            vel = [0, 0]

        self.type = type
        self.colliders = colliders
        self.x = x
        self.y = y
        self.vel = vel
        self.gravity = gravity
        self.friction = friction

        physics_objects.append(self)

    def advance_simulation(self):
        '''advances the phys simulation for this object'''

        if self.type != "immovable":
            self.vel[1] -= self.gravity
            self.move(self.vel[0], self.vel[1])


    def move(self, x: int, y: int):
        '''moves the object by a set amount of pixels'''

        if self.type != "immovable":
            self.x += x
            self.y += y

    def add_vel(self, x: int, y: int):
        '''adds a velocity to this object'''

        if self.type != "immovable":
            self.vel[0] += x
            self.vel[1] += y

    def delete_self(self):
        '''removes this object on the next frame'''
        remove_phys_obj(self)

    # default, meant to be extended
    def handle_trigger(self, collided_obj, my_collider, other_collider): #noqa
        pass

    def handle_collision(self, collided_obj,
                         my_collider, other_collider, handled=False):
        '''handles a collision with another object'''

        # don't collide with self. allows overlapping hitboxes
        if collided_obj is self:
            return

        if my_collider.type == 'trigger':
            self.handle_trigger(collided_obj, my_collider, other_collider)
            return

        if not handled and other_collider.type != "trigger":

            displacement = get_collision_displacement(my_collider, other_collider)

            # nullify velocities in the direction of collision
            if displacement[0] != 0:
                collided_obj.vel[0] = 0
                self.vel[0] = 0

            elif displacement[1] != 0:
                if displacement[1] < 0:
                    collided_obj.vel[1] = max(0, collided_obj.vel[1])
                    self.vel[1] = min(0, self.vel[1])
                else:
                    collided_obj.vel[1] = min(0, collided_obj.vel[1])
                    self.vel[1] = max(0, self.vel[1])

            # can't do anything in this case. Shouldn't even happen tbh
            if collided_obj.type == "immovable" and self.type == "immovable":
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


class Collider():
    '''dataclass that has all of the info about 1 collider'''
    x = 0
    y = 0
    width = 0
    height = 0
    id = "default"
    type = "rigid"
    parent = None

    def __init__(self, x: float, y: float,
                 parent: PhysicsObject,
                 width: float, height: float,
                 id: str = "default", type: str = "rigid"):
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
        '''removes this object from the physics simulation on the next tick'''
        self.parent.colliders.pop(self.id)
        colliders.remove(self)

    # helper functions for edges of the collider

    def left_edge(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return self.x+self.parent.x

    def right_edge(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return self.x+self.width+self.parent.x

    def bottom_edge(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return self.y+self.height+self.parent.y

    def top_edge(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return self.y+self.parent.y

    # helper functions to get locations of all points

    def NW(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return [self.x+self.parent.x, self.y+self.parent.y]

    def NE(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return [self.x+self.width+self.parent.x, self.y+self.parent.y]

    def SW(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return [self.x+self.parent.x, self.y+self.height+self.parent.y]

    def SE(self): #noqa, one-line self-explanatory functions do not need a docstring, pylint
        return [self.x+self.width+self.parent.x, self.y+self.height+self.parent.y]

def get_collision_displacement(my_collider, other_collider):
    '''return by how much this object should be displaced in order to move it outside the another object'''
    global COLLIDER_ACTIVE_BOUNDARY

    top_dist = my_collider.bottom_edge()-other_collider.top_edge()
    bottom_dist = other_collider.bottom_edge() - my_collider.top_edge()
    right_dist = my_collider.right_edge() - other_collider.left_edge()
    left_dist = other_collider.right_edge() - my_collider.left_edge()

    if right_dist < COLLIDER_ACTIVE_BOUNDARY\
            and right_dist > 0\
            and right_dist < top_dist\
            and right_dist < bottom_dist:
        return [-right_dist, 0]

    elif left_dist < COLLIDER_ACTIVE_BOUNDARY\
            and left_dist > 0\
            and left_dist < top_dist\
            and left_dist < bottom_dist:
        return [left_dist, 0]

    elif top_dist < COLLIDER_ACTIVE_BOUNDARY and top_dist > 0:
        return [0, -top_dist]

    elif bottom_dist < COLLIDER_ACTIVE_BOUNDARY and bottom_dist > 0:
        return [0, bottom_dist]

    return [0, 0]

def _colliders_intersect(A: Collider, B: Collider):
    # check if starting point of one rectangle is within projection another on x
    A_SW, A_NE = A.SW(), A.NE()
    B_SW, B_NE = B.SW(), B.NE()
    if (A_SW[0] >= B_NE[0]
            or A_NE[0] <= B_SW[0]
            or A_SW[1] <= B_NE[1]
            or A_NE[1] >= B_SW[1]):
        return False
    else:
        return True


def _handle_all_collisions(arr: list):
    ''''''
    # compare every element in rect list to every next element
    # which gives us total of (n-1)^2 / 2 number of comparisons
    for i, obj in enumerate(arr):
        for obj2 in arr[:i+1]:
            if _colliders_intersect(obj, obj2):
                obj.parent.handle_collision(obj2.parent, obj, obj2, True)
                obj2.parent.handle_collision(obj.parent, obj2, obj, False)


def advance_phys_simulation():
    '''advances the physics simulation by 1 frame'''
    for obj in physics_objects:
        obj.advance_simulation()

    _handle_all_collisions(colliders)
    _remove_phys_obj()


def _remove_phys_obj():
    '''does all sheduled deletions'''
    global _removing
    for phys_obj in _removing:
        for collider in list(phys_obj.colliders.values()):
            collider.delete_self()

        physics_objects.remove(phys_obj)

    _removing = []


def remove_phys_obj(phys_obj):
    '''shedules the deletion of passed obj on the next frame'''
    _removing.append(phys_obj)
