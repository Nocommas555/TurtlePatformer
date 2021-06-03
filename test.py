'''
    Basic test scene made using Chelone
'''
import random
import math
import json
import tkinter as tk

from time import time

from Chelone import init, Sprite, SpriteLoader, check_keys
from BoxPhys import get_collision_displacement


chelone = None
playsound = lambda a: 0
sound_finished = lambda a: False

class Player(Sprite):
    """
        A class for the main character.
        Handles smooth camera, game over, movement and attacks
    """

    grounded = False
    w_pressed = False
    camera_lagbehind = [0.01, 0.05]
    camera_offset = [600, 250]

    def setup(self, kargs):
        print("setup Player")

        # set up anim states
        self.states = {"run": self.run_state, "idle": self.idle_state, "jump": self.jump_state}

        self.grounded = False
        self.w_pressed = False
        self.orientation = "right"

        self.camera_lagbehind = kargs.get("camera_lagbehind", [0.05, 0.05])

        self.camera_offset = kargs.get("camera_offset", [600, 250])

    def update(self):
        if self.anim_state == "None":
            self.update_anim_state('idle')

        self.update_smooth_camera()

    def last_update(self):
        self.grounded = False

    def run_state(self):
        '''the code that runs while the player is running'''
        movement = self.move_on_command()
        if not movement[0] and not movement[1]:
            self.update_anim_state('idle')
        if chelone.settings["jump"] in chelone.pressed_keys and self.grounded:
            self.update_anim_state('jump')
            self.add_vel(0, -30)

    def idle_state(self):
        '''the code that runs while the player is idling'''
        movement = self.move_on_command()
        if movement[0] or movement[1]:
            self.update_anim_state('run')
        if chelone.settings["jump"] in chelone.pressed_keys and self.grounded:
            self.update_anim_state('jump')
            self.add_vel(0, -30)

    def jump_state(self):
        '''the code that runs while the player is jumping'''
        movement = self.move_on_command()#noqa could be used later
        if self.grounded:
            self.update_anim_state('idle')

    def update_smooth_camera(self):
        '''handles updating the camera position smoothly'''
        camera_desired = [
            self.x-self.camera_offset[0],
            self.y-self.camera_offset[1]
        ]

        chelone.camera.move(
            -self.camera_lagbehind[0]*(chelone.camera.x-camera_desired[0]),
            self.camera_lagbehind[1]*(chelone.camera.y-camera_desired[1])
        )

    def move_on_command(self):
        '''handles movement with keypresses'''
        ret = [False, False]

        if chelone.settings['run_left'] in chelone.pressed_keys:
            ret[0] = True
            self.move(-7, 0)

            if self.orientation != "left":
                self.flip()

        elif chelone.settings['run_right'] in chelone.pressed_keys:
            ret[1] = True
            self.move(7, 0)

            if self.orientation != "right":
                self.flip()

        return ret

    def handle_collision(self, collided_obj, my_collider, other_collider, handled=False, displacement = None):
        '''check if we ever intersect ground to be able to jump'''
        if displacement is None:
            displacement = get_collision_displacement(my_collider, other_collider)

        super().handle_collision(collided_obj, my_collider, other_collider, handled, displacement)

        if displacement[1] < 0 and self.vel.y >= 0:
            if my_collider.type != "trigger" and other_collider.type != "trigger":
                self.grounded = True

    def delete_self(self):
        '''
        instead of deleting, we need to pause and restart the game
        TODO: this is a POC, needs to be remade properly
        '''

        print("game_over")
        saved_sprites = chelone._sprites
        chelone._sprites = [{} for i in range(50)]
        game_over = Sprite(
            id="game_over", frame=self.frame.parent.load("game_over.png"),
            x=450+chelone.camera.x, y=chelone.camera.y, phys_type="immovable", layer=1,
        )
        chelone.add_sprite(game_over, 1)


        # loop while dead
        while "Return" not in chelone.pressed_keys:
            check_keys()
            chelone.root.update()

        chelone.next_frame = time()
        chelone.now = time()
        chelone._sprites = saved_sprites

        super().delete_self()

        player = Player(
            id="Player", frame=self.frame.parent.load("tmp.png"),\
            x=250, y=0, gravity=self.gravity,\
            state_anim_directory=self.state_anim_directory
        )
        chelone.add_sprite(player)
        game_over.delete_self()


class Droid(Sprite):
    """
        Basic enemy. Partrols an area and shoots the player if it sees him.
    """

    class Laser(Sprite):
        """
            Projectile that the Droid enemy shoots.
        """
        def setup(self, kargs):
            self.velocity = kargs.get("velocity", [-3, 0])
            self.gravity = 0

        def update(self):
            self.move(self.velocity[0], self.velocity[1])

        def handle_trigger(self, collided_obj, my_collider, other_collider):
            if not isinstance(collided_obj, Droid):
                self.delete_self()
                collided_obj.delete_self()
                print("Laser attacked " + collided_obj.id)


    def setup(self, kargs):
        self.states = {"walk": lambda:0}
        self.patrol_range = kargs.get("patrol_range", [self.x-300, self.x])
        self.speed = kargs.get("speed", 0)
        self.shooting_cooldown_limit = kargs.get("shooting_cooldown", 240)
        self.shooting_cooldown = self.shooting_cooldown_limit

        # make sure we spawn in our patrol range
        self.move(self.patrol_range[1] - self.x, 0)
        self.orientation = "left"


    def update(self):
        if self.anim_state == "None":
            self.update_anim_state('walk')

        if self.shooting_cooldown >= self.shooting_cooldown_limit:
            if self.orientation == "left":
                self.move(-self.speed, 0)
            else:
                self.move(self.speed, 0)

        if self.x < self.patrol_range[0] and self.orientation == "left":
            self.flip()

        elif self.x > self.patrol_range[1] and self.orientation == "right":
            self.flip()

        if self.shooting_cooldown < self.shooting_cooldown_limit:
            self.shooting_cooldown += 1


    def handle_trigger(self, collided_obj, my_collider, other_collider):

        if isinstance(collided_obj, Player) and not isinstance(collided_obj, Droid):
            if self.shooting_cooldown >= self.shooting_cooldown_limit:
                self.shooting_cooldown = 0
                if my_collider.id == "left_search":
                    laser_x = self.x-50
                    laser_vel = -3

                elif my_collider.id == "right_search":
                    laser_x = self.x+self.colliders['collider_1'].width+50
                    laser_vel = 3

                self.Laser(
                    id="Laser", frame=self.frame.parent.load("laser.png"), gravity=0,
                    x=laser_x,
                    y=self.y+self.colliders['collider_1'].height/2,
                    velocity=[laser_vel, 0]
                )

class background_sound(Sprite):
    '''loops the bg music'''
    def setup(self, kargs):

        self.sound = kargs['sound']

        self.playing_sound = playsound(self.sound)

    def update(self):

        if sound_finished(self.playing_sound):
            self.playing_sound = playsound(self.sound)

def droid_generator(droid_x, droid_quantity):
    '''generates multiple droids'''
    loader = SpriteLoader()

    for i in range(1, droid_quantity):
        patrol_range = [droid_x + 100, droid_x + 200]
        Droid("Droid", loader.load("droid.png"), patrol_range=patrol_range, speed=1.3, state_anim_directory = "droid")
        droid_x += 90


def block_generator(block_x, block_quantity, ground_y):
    '''generates a block pile'''
    loader = SpriteLoader()

    for i in range(1, block_quantity - 1):
        Sprite("Block", loader.load("box.png"), phys_type="immovable", x = block_x, y=ground_y - 60, layer = 26)
        Sprite("Block", loader.load("box.png"), phys_type="immovable", x = block_x + 50, y=ground_y - 135)
        block_x += 100

    Sprite("Block", loader.load("box.png"), phys_type="immovable", x = block_x, y=ground_y - 60, layer = 26)

def level_generator(start_x = 0, obj_quantity = 1, ground_y = 650):
    '''generating simple levels from patterns found in level_patterns.json'''
    loader = SpriteLoader()

    try:
        pattern = json.load(open("level_patterns.json", "r"))
    except Exception as e:
        pattern = []
        print(e)

    b = 0
    i = 0
    obj_x = 0

    while b < obj_quantity:
        selected_sector = pattern[random.randint(0, len(pattern) - 1)]
        obj_x += selected_sector["width"]
        block_generator(obj_x, selected_sector["block_quantity"], ground_y)
        droid_generator(obj_x + 300, selected_sector["droid_quantity"])
        b += 1

    while i < math.ceil(obj_x/2560.0):
        Sprite("Ground", loader.load("gnd.png"), phys_type="immovable", x=start_x, y=ground_y, layer=49)
        start_x += 2560
        i += 1



def start_level(root = None):
    '''main function for loading the level'''
    global chelone, playsound, sound_finished

    # setting up global objects for rendering and loading, respectively
    chelone = init(root)

    loader = SpriteLoader()

    Player("Player", loader.load("tmp.png"), gravity=-1, x=400, y=400, layer=10, state_anim_directory="anakin")

    if chelone.settings["sound"]:
        import sound
        playsound = sound.playsound
        sound_finished = sound.sound_finished

    level_generator(obj_quantity=30)

    background_sound("background", loader.load("clear.png"), phys_type="inmovable", sound="sounds/imperial_march.wav")

    fps_tracker = tk.Label(root, text = 'fps')
    fps_tracker.config(font=("sans-serif", 44))
    fps_tracker.place(relx=0, rely=0, anchor=tk.NW)

    while 1:
        startTime = time()
        chelone.advance_frame()
        endTime = time()
        elapsedTime = endTime - startTime
        #print(1./elapsedTime)
        fps_tracker.config(text = str(int(1./elapsedTime)))



if __name__ == '__main__':
    start_level()
