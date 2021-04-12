'''
    Basic test scene made using Chelone
'''
from time import time

from Chelone import init, Sprite, SpriteLoader, check_keys
from sound import playsound, sound_finished, sounds #noqa, will be used later


# setting up global objects for rendering and loading, respectively
chelone = init(1600, 800)
loader = SpriteLoader()

class Player(Sprite):
    """
        A class for the main character.
        Handles smooth camera, game over, movement and attacks
    """

    grounded = False
    w_pressed = False
    camera_lagbehind = [0.01, 0.05]
    camera_offset = [600, 300]

    def setup(self, kargs):
        print("setup Player")

        # set up anim states
        self.states = {"run": self.run_state, "idle": self.idle_state}
        self.anim_state = "idle"

        self.grounded = False
        self.w_pressed = False
        self.orientation = "right"

        self.camera_lagbehind = kargs.get("camera_lagbehind", [0.05, 0.05])

        self.camera_offset = kargs.get("camera_offset", [600,300])
        
    def update(self):

        if 'w' in chelone.pressed_keys and\
          self.grounded and not self.w_pressed:

            self.add_vel(0, -30)

        self.update_smooth_camera()

        self.grounded = False
        self.w_pressed = 'w' in chelone.pressed_keys

    def run_state(self):
        movement = self.move_on_command()
        if not movement[0] and not movement[1]:
            self.update_anim_state('idle')

    def idle_state(self):
        movement = self.move_on_command()
        if movement[0] or movement[1]:
            self.update_anim_state('run')

    # smooth camera follow
    def update_smooth_camera(self):
        camera_desired = [
            self.x-self.camera_offset[0],
            self.y-self.camera_offset[1]
        ]

        chelone.camera.move(
            -self.camera_lagbehind[0]*(chelone.camera.x-camera_desired[0]),
            self.camera_lagbehind[1]*(chelone.camera.y-camera_desired[1])
        )


    def move_on_command(self):
        ret = [False, False]
        if 'a' in chelone.pressed_keys:
            ret[0] = True
            self.move(-7, 0)

            if self.orientation != "left":
                self.flip()

        elif 'd' in chelone.pressed_keys:
            ret[1] = True
            self.move(7, 0)

            if self.orientation != "right":
                self.flip()
        
        return ret

    def handle_collision(self, collided_obj, my_collider, other_collider, handled=False):
        displacement = self.get_collision_displacement(collided_obj, my_collider, other_collider)
        super().handle_collision(collided_obj, my_collider, other_collider, handled)

        # pylint: disable=chained-comparison
        if displacement[1] < 0 and self.vel[1] >= 0:
            if my_collider.type != "trigger" and other_collider.type != "trigger":
                self.grounded = True

    def delete_self(self):
        print("game_over")
        saved_sprites = chelone._sprites
        chelone._sprites = [{} for i in range(50)]
        game_over = Sprite(
            id="game_over", frame=loader.load("game_over.png"),
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
            id="Player", frame=loader.load("tmp.png"),\
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

        self.patrol_range = kargs.get("patrol_range", [self.x-300, self.x])
        self.speed = kargs.get("speed", 0)
        self.shooting_cooldown_limit = kargs.get("shooting_cooldown", 240)
        self.shooting_cooldown = self.shooting_cooldown_limit

        # make sure we spawn in our patrol range
        self.move(self.patrol_range[1] - self.x, 0)
        self.orientation = "left"


    def update(self):
        if self.shooting_cooldown >= self.shooting_cooldown_limit:
            if self.orientation == "left":
                self.move(-self.speed, 0)
            else:
                self.move(self.speed, 0)

        if self.x < self.patrol_range[0]:
            self.orientation = "right"

        elif self.x > self.patrol_range[1]:
            self.orientation = "left"

        if self.shooting_cooldown < self.shooting_cooldown_limit:
            self.shooting_cooldown += 1


    def handle_trigger(self, collided_obj, my_collider, other_collider):

        if isinstance(collided_obj, Player):
            if self.shooting_cooldown >= self.shooting_cooldown_limit:
                self.shooting_cooldown = 0
                if my_collider.id == "left_search":
                    self.Laser(
                        id="Laser", frame=loader.load("laser.png"), gravity=0,
                        x=self.x-50,
                        y=self.y+self.colliders['body'].height/2,
                        velocity=[-3, 0]
                    )

                elif my_collider.id == "right_search":
                    self.Laser(
                        id="Laser", frame=loader.load("laser.png"), gravity=0,
                        x=self.x+self.colliders['body'].width+50,
                        y=self.y+self.colliders['body'].height/2,
                        velocity=[3, 0]
                    )


class background_sound(Sprite):

    def setup(self, kargs):

        self.sound = kargs['sound']

        self.playing_sound = playsound(self.sound)

    def update(self):

        if(sound_finished(self.playing_sound)):
            self.playing_sound = playsound(self.sound)


spr = Player("Player", loader.load("tmp.png"), gravity=-1, x=100, layer=10, state_anim_directory="anakin")

background_sound("background", loader.load("clear.png"), phys_type = "inmovable", sound = "sounds/imperial_march.wav") 

drd1 = Droid("Droid", loader.load("droid.png"), patrol_range=[700, 1300], speed=1)

#drd2 = Droid_1("Droid 2", loader.load("droid.png"), x = 1200)
#chelone.add_sprite(drd2)

#drd3 = Droid_1("Droid 3", loader.load("droid.png"), x = 1400)
#chelone.add_sprite(drd3)

ground = Sprite("Ground", loader.load("gnd.png"), phys_type="immovable", x=0, y=650, layer=49)

block = Sprite("Block", loader.load("tmp.png"), phys_type="immovable", x=500, y=350)

# movable = Sprite("Movable", loader.load("tmp.png"), x=150, y=200)
# chelone.add_sprite(movable, 30)

#laser = Laser("Laser", loader.load("laser.png"), x = 900)
#chelone.add_sprite(laser)

while 1:
    startTime = time()
    chelone.advance_frame()
    endTime = time()
    elapsedTime = endTime - startTime
