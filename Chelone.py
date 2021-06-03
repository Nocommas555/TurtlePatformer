'''
Chelone is a graphics library created specifically for our platformer
It is a wrapper over the included tkinter library that seeks to become an
alternative to pyGame with more of a focus on sprites rather then  primitives

The engine includes basic loading, collision detection, animation, drawing, z-layering and complex backrounds
'''
import tkinter as tk
import os
import json
from typing import Union, Callable
from time import time, sleep

from sound import kill_all_sounds
from BoxPhys import Collider, PhysicsObject, advance_phys_simulation, reset_phys_sim, SIMILATION_RADIUS

chelone = None
resolution_x = 1600
resolution_y = 800

def init(root = None):
    '''initializes the tk screen, canvas and SpriteRenderer class'''
    global chelone, resolution_x, resolution_y

    # Create the window with the Tk class
    if root is None:
        root = tk.Tk()
    else:
        for child in root.winfo_children():
            child.destroy()

    if chelone is None:
        root.protocol("WM_DELETE_WINDOW", exit)
        root.bind("<Key>", on_key_press)
        root.bind("<KeyRelease>", on_key_release)
        root.bind("<FocusOut>", FocusOut)
                
        # Create the canvas and make it visible with pack()
        canvas = tk.Canvas(root, width=resolution_x, height=resolution_y)
        canvas.pack()

        chelone = SpriteRenderer(root, canvas)

    else:
        chelone.reset()


    return chelone

def exit():
    '''exits the program'''
    kill_all_sounds()
    chelone.root.destroy()
    os._exit(0) #noqa exit forcefully to shut down child processes that play sounds

def FocusOut(event): # noqa, event var needed for callback signature
    ''' clears input on unfocusing window. should maybe halt the game in the future '''
    chelone.caught_keys_prev = []
    chelone.caught_keys = []
    chelone.pressed_keys = []


def check_keys():
    '''debouncer for buggy built-in key detection'''

    # remove keys not caught for 2 frames
    for key in chelone.pressed_keys:
        if key not in chelone.caught_keys and\
          key not in chelone.caught_keys_prev:

            chelone.pressed_keys.remove(key)

    # add keys that are not already pressed
    for key in chelone.caught_keys:
        if key not in chelone.pressed_keys:
            chelone.pressed_keys.append(key)

    # save current keys to check the next
    chelone.caught_keys_prev = chelone.caught_keys.copy()


def on_key_press(event): # noqa, event var needed for callback signature
    '''handles capturing key presses'''
    if event.keysym not in chelone.caught_keys:
        chelone.caught_keys.append(event.keysym)


def on_key_release(event): # noqa, event var needed for callback signature
    '''handles capturing key releases'''
    chelone.caught_keys.remove(event.keysym)


class SpriteLoader():
    '''
    Handles loading sprites and animations
    There can be multiple instances at the same time
    '''
    _sprite_dir = "/sprites"
    _storage = {}


    class SpriteFrame():
        '''A frame of animation that has extra data for collision detection'''
        hitboxes = {}
        extra = {}
        image = None
        path = ""
        parent = None

        def __init__(self, file: str, parent, hitboxes: list = None, extra: dict = None):

            if hitboxes is None:
                hitboxes = []

            if extra is None:
                extra = {}

            self.image = tk.PhotoImage(file=file)
            self.hitboxes = hitboxes
            self.extra = extra
            self.path = file
            self.parent = parent


    def __init__(self, sprite_dir: str = "sprites/"):
        self._sprite_dir = sprite_dir
        self._storage = {}

    def load_anim(self, path: str):
        '''loads animation as an array of paths to frames'''

        if os.path.exists(self._sprite_dir+path):
            return[
                "/".join(path.split("/")[:-1])+"/"+x
                if x != "None" else None
                for x in json.load(open(self._sprite_dir+path))
            ]

        else:
            print("wrong anim path: " + path)
            return [None]

    def load(self, path: str):
        '''loads a SpriteFrame from a relative path'''

        path = self._sprite_dir + path

        # check if we already loaded the image
        if path in self._storage.keys():
            return self._storage[path]

        parent_path = "/".join(path.split("/")[:-1])
        file = path.split("/")[-1]

        if os.path.exists(path) and os.path.exists(parent_path+'/'+"img_descr.json"):

            img_descr = json.load(open(parent_path+'/'+"img_descr.json"))["images"][file]

            if os.path.isfile(path):

                hitboxes = {}
                if "hitboxes" in img_descr:
                    hitboxes = img_descr["hitboxes"]

                extra = {}
                if "extra" in img_descr:
                    extra = img_descr["extra"]

                self._storage[path] = self.SpriteFrame(path, self, hitboxes, extra)

                if "scale" in img_descr:
                    self._storage[path].image = self._storage[path].image.zoom(img_descr["scale"])

                return self._storage[path]

        print("SPRITE NOT FOUND AT: " + path + " or " + parent_path+"/img_descr.json")
        return None

    def unload(self, path: str):
        '''remove all loaded Frames from memory. will cause the associated picture to dissapear on the canvas'''
        self._storage.pop(path)

    def unload_all(self):
        '''unloads all Frames'''

        for path in self._storage:
            self.unload(path)

class AnimStateSystem():
    '''interface for handling anim state changes and their functions'''
    states = {}
    state_anim_directory = ""
    _anim_frame = 0
    _anim = []
    orientation = 'right'

    def __init__(self, state_anim_directory: str):

        self.states["None"] = lambda: 0 # noop
        self.state_anim_directory = state_anim_directory
        self.anim_state = "None"
        self._anim_frame = 0
        self._anim = []

    def flip(self):
        '''flips the current animation and changes the orientation'''
        if self.orientation == "left":
            self.orientation = "right"
        else:
            self.orientation = "left"

        if self.anim_state != "None":
            anim_name = self.state_anim_directory + "/" + self.anim_state + "_" + self.orientation + ".anim"
            self.start_anim(anim_name, self._anim_frame)


    def _update_state(self):
        '''triggers the state update function'''
        self.states[self.anim_state]()

    def update_anim_state(self, state):
        '''updates anim_state and starts the associated anim'''
        self.anim_state = state
        if state != "None":
            self.start_anim(self.state_anim_directory + "/" + state + "_" + self.orientation + ".anim")

    def start_anim(self, anim_frames: Union[str, list], start: int = 0): #noqa, meant to be extended
        pass

class Sprite(PhysicsObject, AnimStateSystem):
    '''Basic scene object. Intended to be inherited to extend functionality'''
    x = 0
    y = 0
    frame = None
    image_tk = None
    parent_canvas = None
    _anim = []
    _anim_frame = 0
    id = ""
    _current_offset = {"x":0, "y":0}

    # updateFunc is a function that takes self and gets called every frame
    # setupFunc is a function that takes self and gets called once, at setup

    def __init__(self, id: str, frame: SpriteLoader.SpriteFrame,
                 x: int = 0, y: int = 0, phys_type: str = "default", gravity: float = -0.3, friction: float = 0.1,
                 layer: int = 25, state_anim_directory: str = ".", **kargs):

        PhysicsObject.__init__(self, phys_type, {}, x, y, [0, 0], gravity, friction)

        self.id = chelone.get_unique_id(id)

        self.layer = 25
        self.frame = frame
        self.image_tk = None
        self.parent_canvas = None
        self._current_offset = {"x":0, "y":0}
        self.states = {}
        self.orientation = "right"
        self.anim_state = "None"

        self.create_colliders()
        chelone.add_sprite(self, layer)

        self.setup(kargs)

        # because setup should define anim states, we should setup AnimStateSystem after
        AnimStateSystem.__init__(self, state_anim_directory=state_anim_directory)

        self._anim = [frame]
        self._anim_frame = 0

    # made to be extended
    def setup(self, kargs): #noqa
        pass

    # made to be extended
    def update(self): #noqa
        pass

    # made to be extended
    def last_update(self): #noqa
        pass

    def delete_self(self):
        '''deletes this object and it's colliders'''

        PhysicsObject.delete_self(self)
        self.parent_canvas.delete(self.image_tk)
        chelone.remove_sprite(self)

    def update_active(self):
        self.active = abs(self.x-chelone.camera.x)<SIMILATION_RADIUS

    def update_all(self):
        '''function to call everything that needs to be updated in a frame'''

        if self.active:
            self.update()
            self.advance_anim()
            self._update_state()
            self.last_update()

    def move(self, x: int, y: int):
        '''moves the sprite a set amount of pixels'''
        self.x += x
        self.y += y
        self.parent_canvas.move(self.image_tk, x, y)

    def create_colliders(self):
        '''creates/updates colliders of a Sprite using it's current Frame hitbox parameters'''

        for key in self.frame.hitboxes.keys():
            hitbox = self.frame.hitboxes[key]

            if hitbox == "remove":
                self.colliders[key].delete_self()

            else:
                if key in self.colliders:
                    self.colliders[key].delete_self()

                self.colliders[key] = Collider(hitbox["x"], hitbox["y"],\
                    self, hitbox["width"], hitbox["height"], key, hitbox["type"])

    def change_image(self, frame: SpriteLoader.SpriteFrame, stop_anim: bool = True):
        '''changes the current picture of the sprite'''

        # restore original offset
        if self._current_offset["x"] != 0 or self._current_offset["y"] != 0:
            self.parent_canvas.move(self.image_tk, self._current_offset["x"], self._current_offset["y"])
            self._current_offset["x"] = 0
            self._current_offset["y"] = 0

        self.frame = frame
        self.parent_canvas.itemconfig(self.image_tk, image=frame.image)
        self.create_colliders()

        if stop_anim:
            self._anim = [frame]
            self._anim_frame = 0
            self.update_anim_state("None")

        # offsetting pictures that need it
        if "offset" in self.frame.extra.keys():
            self.parent_canvas.move(self.image_tk, -self.frame.extra["offset"]["x"], -self.frame.extra["offset"]["y"])
            self._current_offset["x"] = self.frame.extra["offset"]["x"]
            self._current_offset["y"] = self.frame.extra["offset"]["y"]


    def start_anim(self, anim_frames: Union[str, list], start: int = 0):
        '''starts a new animation from path to .anim file or array of Frame paths'''

        if isinstance(anim_frames, str):
            anim_frames = self.frame.parent.load_anim(anim_frames)

        self._current_offset["x"] = 0
        self._current_offset["y"] = 0
        self.parent_canvas.delete(self.image_tk)
        self._anim = anim_frames
        self._anim_frame = start

        self.image_tk = self.parent_canvas.create_image(
            self.x-chelone.camera.x, self.y-chelone.camera.y, anchor=tk.NW, image=self.frame.image
            )

    def advance_anim(self):
        '''advances current scheduled animation a frame forward'''

        # check if we are in an anim
        if len(self._anim) > 1:

            # loop animation automatically
            if self._anim_frame >= len(self._anim):
                self._anim_frame = 0

            if self._anim[self._anim_frame] is not None:
                self.change_image(self.frame.parent.load(self._anim[self._anim_frame]), stop_anim=False)

            self._anim_frame += 1


class SpriteRenderer():
    '''Main drawing class. Handles every sprite'''
    root = None
    screen = None
    _sprites = []
    _prev_draw_time = None
    _ids = {}

    caught_keys_prev = []
    caught_keys = []
    pressed_keys = []

    settings = {}

    TARGET_FPS = 60
    camera = None

    DEBUG = True
    debug_flags = [] # opt: hitbox_draw
    DEBUG_ACTIVATION_TIMEOUT = 60
    debug_activation_counter = 0

    class Camera():
        '''dataobject with info about the camera'''
        def __init__(self, screen, x=0, y=0):
            self.x = x
            self.y = y
            self.screen = screen

        def move(self, x, y):
            '''moves the camera'''
            self.x += x
            self.y += -y
            self.screen.move("all", -x, y)


    def __init__(self, root: tk.Tk, screen: tk.Canvas):
        self.root = root
        self.screen = screen
        self.camera = self.Camera(screen)
        self.load_settings()
        # 50 different z layers
        self._sprites = []
        for i in range(50): #noqa, no way to not use i and have a for loop
            self._sprites.append({})

        self.restart_fps_timer()

    def load_settings(self):
        '''load settings from settings.json'''
        #create file if it doesn't exist
        open("settings.json", "a+")

        with open("settings.json", "r") as settings_file:
            try:
                self.settings = json.load(settings_file)
            except:
                self.settings = {"sound": True,
                                "jump": "w",
                                "duck": "s",
                                "run_right": "d",
                                "run_left": "a",
                                "force": "e",
                                "atack": "space"}

    def restart_fps_timer(self):
        '''resets the variables associated with fps waiting'''
        self.frame_period = 1.0/self.TARGET_FPS
        self.now = time()
        self.next_frame = self.now + self.frame_period


    def advance_frame(self):
        '''advance the render, sprite updates and the phys simulation'''
        self.now = time()
        while self.now < self.next_frame:
            sleep(self.next_frame - self.now)
            self.now = time()


        advance_phys_simulation()
        for layer in self._sprites:
            for sprite in layer.values():
                sprite.update_all()


        if self.DEBUG:
            self.check_debug_keys()
            if "hitbox_draw" in self.debug_flags:
                self.db_draw_hitboxes()
            else:
                self.screen.delete("hb")


        self.root.update()
        self.next_frame += self.frame_period

        check_keys()

    def get_unique_id(self, id: str):
        '''returns an unique id'''
        if id not in self._ids:
            self._ids[id] = 1
        else:
            self._ids[id] += 1

        return id + "_" + str(self._ids[id])

    def relayer(self):
        '''realayers all sprites. not the best implementation, works for now'''
        for layer in self._sprites[::-1]:
            for spr in layer.values():
                self.screen.tag_raise(spr.image_tk)

    def add_sprite(self, sprite: Sprite, layer: int = 25):
        '''adds the sprite to the update shedule and automatically layer it'''
        if layer < 1 or layer > 49:
            return

        sprite.layer = layer
        self._sprites[layer][sprite.id] = sprite

        if sprite.image_tk is None:
            sprite.image_tk = self.screen.create_image(
                sprite.x-self.camera.x, sprite.y-self.camera.y, anchor=tk.NW, image=sprite.frame.image
                )

        sprite.parent_canvas = self.screen
        self.relayer()

    def remove_sprite(self, sprite: Sprite):
        '''removes the sprite from the update shedule'''
        if sprite.id in self._sprites[sprite.layer]:
            self._sprites[sprite.layer].pop(sprite.id)

    def bind(self, func: Callable, key: str): #noqa, single-line wrapper
        self.root.bind(func, key)

    def reset(self):
        '''resets the game state to start of level'''
        self.camera.move(-self.camera.x, self.camera.y)

        # reset _sprites array
        for layer in self._sprites:
            for sprite in list(layer):
                layer.pop(sprite)

        reset_phys_sim()
        kill_all_sounds()
        self.screen.delete("all")

    def toggle_debug_flag(self, flag):
        '''changes the state of a debug flag'''
        if flag not in self.debug_flags:
            self.debug_flags.append(flag)
        else:
            self.debug_flags.remove(flag)

        self.debug_activation_counter = 0

    def check_debug_keys(self):
        '''checks if we should toggle a debug flag or not'''
        if self.debug_activation_counter != self.DEBUG_ACTIVATION_TIMEOUT:
            self.debug_activation_counter += 1
            return


        if 'Control_L' in self.pressed_keys and 'b' in self.pressed_keys:
            self.toggle_debug_flag("hitbox_draw")

    def db_draw_hitboxes(self):
        '''draws all active hitboxes as transparent rectangles'''
        colors = {"green":{"outline":"#00bb00", "fill":"#004400"},
                        "red":{"outline":"#bb0000", "fill":"#440000"},
                        "black":{"outline":"#000000", "fill":"#000000"}}

        self.screen.delete("hb")

        for layer in self._sprites:
            for sprite in layer.values():
                for collider in sprite.colliders.values():
                    if collider.type == "trigger":
                        color = "green"
                    elif collider.type == "rigid":
                        color = "red"
                    else:
                        color = "black"

                    x = collider.NW().x-self.camera.x
                    y = collider.NW().y-self.camera.y
                    x2 = collider.SE().x-self.camera.x
                    y2 = collider.SE().y-self.camera.y
                    self.screen.create_rectangle(x, y, x2, y2, fill=colors[color]['fill'], stipple="gray50", tag="hb")
 