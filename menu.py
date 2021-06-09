'''
    Our main menu + settings menu
'''

import tkinter as tk
import tkinter.font as tkfont
import os
import json
from test import start_level
from time import time, sleep
import functools
from random import randint


# set default settings
user_settings = {
    "sound": False,
    "jump": "w",
    "duck": "s",
    "run_right": "d",
    "run_left": "a",
    "force": "e",
    "atack": "space"
}

# init globals
game_not_started = True

sprite_objects = []
current_drag_sprite = None
drag_point = {}

states_label = {
    "sound": False,
    "jump": None,
    "duck": None,
    "run_right": None,
    "run_left": None,
    "force": None,
    "atack": None
}
active_managable_setting = ""

PICTURE_PARENT_DIRECTORY = './menu_pics/'
SETTINGS_FILENAME = 'settings.json'

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800
BACKGROUND_WIDTH = 2600

TARGET_FPS = 30
frame_period = 1.0/TARGET_FPS
frames_lapsed = 0
now = time()
next_frame_time = now + frame_period

# declare classes
class Sprite:
    ''' Pictures in the main screen '''
    anchor_offsets = {
        tk.CENTER: {'x': -0.5, 'y': -0.5},
        tk.NW: {'x': 0, 'y': 0},
        tk.SW: {'x': 0, 'y': -1},
        tk.NE: {'x': -1, 'y': 0},
        tk.SE: {'x': -1, 'y': -1}
    }

    def __init__(
        self, ID="?", x=0, y=0, width=0, height=0,
        anchor=tk.CENTER, img_file=None, parent_frame=None
    ):
        self.ID = ID
        self.x = x + width * self.anchor_offsets[anchor]['x']
        self.y = y + height * self.anchor_offsets[anchor]['y']
        self.width = width
        self.height = height
        self.image = tk.PhotoImage(file=img_file)
        self.instance = parent_frame.create_image(
            x, y, anchor=anchor, image=self.image
        )
        self.parent_frame = parent_frame
        self.last_movement_x = 0
        self.last_movement_y = 0

    def on_click(self, offset_x, offset_y):
        ''' Made to be overriden '''
        pass # noqa , function meant to be extended

    def move(self, dx, dy):
        ''' Moves sprite if needed '''
        self.parent_frame.move(self.instance, dx, dy)
        self.x += dx
        self.y += dy
        self.last_movement_x = dx
        self.last_movement_y = dy

class BackgroundSprite(Sprite):
    

class DragableSprite(Sprite):
    ''' Sprites which you can move with mouse '''
    def on_click(self, offset_x, offset_y):
        global current_drag_sprite

        self.drag_point = {'x': offset_x, 'y': offset_y}
        self.last_movement_x = 0
        self.last_movement_y = 0

        current_drag_sprite = self

class PlayButton(Sprite):
    ''' Button that starts level '''
    def on_click(self, offset_x, offset_y):
        global game_not_started

        main_menu_frame.pack_forget()
        game_not_started = False
        start_level(root)

class SettingsButton(Sprite):
    ''' Button that sends you to settings menu '''
    def on_click(self, offset_x, offset_y):
        change_frame(main_menu_frame, settings_frame)

class ExitButton(Sprite):
    ''' Button that exits program '''
    def on_click(self, offset_x, offset_y):
        os._exit(0) # noqa , only way to kill child processes


# set up screen
root = tk.Tk()
root.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))

main_menu_frame = tk.Canvas(root, bg="black")
main_menu_frame.pack(fill=tk.BOTH, expand=1)

settings_frame = tk.Frame(
    root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black"
)

b_background_sprite = Sprite(
    x=0,
    y=0,
    img_file=PICTURE_PARENT_DIRECTORY+'b_background.png',
    anchor=tk.NW,
    parent_frame=main_menu_frame
)
b_background_sprite_next = Sprite(
    x=BACKGROUND_WIDTH/2,
    y=0,
    img_file=PICTURE_PARENT_DIRECTORY+'b_background.png',
    anchor=tk.NW,
    parent_frame=main_menu_frame
)

sprites_properties = {
    'b_planet_ring':
        {
            'x': randint(0, WINDOW_WIDTH),
            'y': randint(0, WINDOW_HEIGHT),
            'width': 65,
            'height': 97,
            'class': DragableSprite
        },
    'b_planet':
        {
            'x': randint(0, WINDOW_WIDTH),
            'y': randint(0, WINDOW_HEIGHT),
            'width': 57,
            'height': 57,
            'class': DragableSprite
        },
    'b_death_star':
        {
            'x': randint(0, WINDOW_WIDTH),
            'y': randint(0, WINDOW_HEIGHT),
            'width': 176,
            'height': 176,
            'class': DragableSprite
        },
    '1_title_image':
        {
            'x': WINDOW_WIDTH*0.765,
            'y': WINDOW_HEIGHT*0.3,
            'width': 0,
            'height': 0,
            'class': Sprite
        },
    'm_play':
        {
            'x': WINDOW_WIDTH*0.5,
            'y': WINDOW_HEIGHT*0.6,
            'width': 228,
            'height': 100,
            'class': PlayButton
        },
    'm_settings':
        {
            'x': WINDOW_WIDTH*0.5,
            'y': WINDOW_HEIGHT*0.75,
            'width': 169,
            'height': 50,
            'class': SettingsButton
        },
    'm_exit':
        {
            'x': WINDOW_WIDTH*0.5,
            'y': WINDOW_HEIGHT*0.85,
            'width': 100,
            'height': 50,
            'class': ExitButton
        }
}
for sprite_name in sprites_properties:
    sprite_property = sprites_properties[sprite_name]
    img_location = PICTURE_PARENT_DIRECTORY+sprite_name+'.png'

    sprite_objects.append(
        sprite_property['class'](
            x=sprite_property['x'],
            y=sprite_property['y'],
            width=sprite_property['width'],
            height=sprite_property['height'],
            img_file=img_location,
            parent_frame=main_menu_frame
        )
    )


# reverse order of objects,
# so that ones which are on top have higher interaction priority
sprite_objects.reverse()

regular_font = tkfont.Font(family='Noto Sans Display', size=16)


# main functional
def load_settings():
    ''' Loads settings '''
    global user_settings

    open(SETTINGS_FILENAME, "a+")
    try:
        user_settings = json.load(open(SETTINGS_FILENAME))
    except:
        pass

def save_settings():
    ''' Saves settings '''
    global user_settings

    # create file if not found
    open(SETTINGS_FILENAME, "a+")

    json.dump(user_settings, open(SETTINGS_FILENAME, "w"))


def change_frame(this_frame, next_frame):
    ''' Changes frame '''
    this_frame.pack_forget()
    next_frame.pack(fill=tk.BOTH, expand=1)
    root.update()

def click_on_sprite_main_menu(event):
    ''' Detects if user clicked on sprite in main menu '''
    for obj in sprite_objects:
        if obj.x < event.x < obj.x + obj.width\
        and obj.y < event.y < obj.y + obj.height:
            obj.on_click(obj.x - event.x, obj.y - event.y)

def drag_sprite(event):
    ''' Moves movable sprite while mouse clicked and moving '''
    for obj in sprite_objects:
        if isinstance(obj, DragableSprite):
            if obj is current_drag_sprite:
                obj.move(
                    event.x + obj.drag_point["x"] - obj.x,
                    event.y + obj.drag_point["y"] - obj.y
                )

def release_sprite(event): # noqa , parameter event needed for callback signature
    ''' Stops current movable sprite from moving when unclicked '''
    global current_drag_sprite

    current_drag_sprite = None

def flip_sound_setting():
    ''' Turns sound off if it`s turned on,
        and turns sound on if it`s turned off '''
    global user_settings

    user_settings["sound"] = not user_settings["sound"]

    on_label = tk.Label(
        master=settings_frame,
        text='ON',
        font=regular_font,
        fg='white',
        bg='green'
    )
    off_label = tk.Label(
        master=settings_frame,
        text='OFF',
        font=regular_font,
        fg='black',
        bg='red'
    )

    sound_label = on_label if user_settings["sound"] else off_label

    sound_label.place(
        relx=0.5,
        rely=0.17,
        width=WINDOW_WIDTH*0.1,
        height=WINDOW_HEIGHT*0.07,
        anchor=tk.CENTER
    )

    save_settings()

def on_key_press(event):
    ''' Reasignes control key of a selected action '''
    global active_managable_setting, states_label

    if active_managable_setting != "":
        states_label[active_managable_setting].configure(text=event.keysym)
        user_settings[active_managable_setting] = event.keysym
        active_managable_setting = ""
        save_settings()
    else:
        return

def update_manage_setting(state_parameter):
    ''' Detects which action is changes control key '''
    global active_managable_setting

    active_managable_setting = state_parameter

def add_button_with_label(
    master=settings_frame,
    text="?", font=regular_font, foreground="blue",
    command=None, function_arguments=(),
    relx=0.5, rely=0.5,
    button_width=150, button_height=50,
    label_width=150, label_height=50,
    anchor=tk.CENTER,
    ID="unnamed"
):
    ''' Adds button and it`s corresponding label '''
    tk.Button(
        master=master,
        text=text,
        font=font,
        fg=foreground,
        command=functools.partial(command, function_arguments)
    ).place(
        relx=(relx-button_width/WINDOW_WIDTH)/2,
        rely=rely,
        width=button_width,
        height=button_height,
        anchor=anchor
    )
    states_label[ID]=tk.Label(
        master=master,
        text=user_settings[ID],
        font=font,
        fg=foreground,
    )
    states_label[ID].place(
        relx=relx*1.01+(button_width/WINDOW_WIDTH)/2,
        rely=rely*1.01,
        width=label_width,
        height=label_height,
        anchor=anchor
    )

def restart_fps_timer():
    ''' Resets the variables associated with fps waiting '''
    global now, next_frame_time

    now = time()
    next_frame_time = now + frame_period

def animate_background():
    ''' Animates stars and palnets on the background '''
    global b_background_sprite, b_background_sprite_next,\
        frames_lapsed, now, next_frame_time

    now = time()
    while now < next_frame_time:
        sleep(next_frame_time - now)
        now = time()

    next_frame_time = now + frame_period
    frames_lapsed += 1

    for image in (b_background_sprite, b_background_sprite_next):
        image.move(-1, 0)

    if frames_lapsed >= BACKGROUND_WIDTH / 2:
        # kinda reset

        b_background_sprite = b_background_sprite_next
        b_background_sprite_next = Sprite(
            x=BACKGROUND_WIDTH/2,
            y=0,
            img_file=PICTURE_PARENT_DIRECTORY+'b_background.png',
            anchor=tk.NW,
            parent_frame=main_menu_frame
        )
        main_menu_frame.lower(b_background_sprite_next.instance)
        frames_lapsed = 0

    # inertia implentation
    for obj in sprite_objects:
        if obj is not current_drag_sprite:
            obj.move(obj.last_movement_x, obj.last_movement_y)

    root.update()

# make some preparations
load_settings()
flip_sound_setting()
flip_sound_setting()

# set up settings UI
tk.Button(
    master=settings_frame,
    text='Sound',
    font=regular_font,
    fg='blue',
    command=flip_sound_setting
).place(
    relx=0.5,
    rely=0.1,
    width=WINDOW_WIDTH*0.15,
    height=WINDOW_HEIGHT*0.07,
    anchor=tk.CENTER
)

tk.Button(
    master=settings_frame,
    text='Return to main menu',
    font=regular_font,
    fg='blue',
    command=lambda:change_frame(settings_frame, main_menu_frame)
).place(
    relx=0.5,
    rely=0.8,
    width=WINDOW_WIDTH*0.2,
    height=WINDOW_HEIGHT*0.07,
    anchor=tk.CENTER
)

control_button_rely = 0.3
delta_rely = 0.07
for key in user_settings:
    if key == 'sound':
        continue

    add_button_with_label(
        text=key,
        command=update_manage_setting,
        function_arguments=(key),
        relx=0.5,
        rely=control_button_rely,
        button_width=WINDOW_WIDTH*0.1,
        button_height=WINDOW_HEIGHT*delta_rely*0.9,
        label_width=WINDOW_WIDTH*0.1,
        label_height=WINDOW_HEIGHT*delta_rely*0.9,
        ID=key
    )
    control_button_rely += delta_rely


bind_dict = {
    '<Button-1>': click_on_sprite_main_menu,
    '<B1-Motion>': drag_sprite,
    '<B1-ButtonRelease>': release_sprite
}
for action in bind_dict:
    main_menu_frame.bind(action, bind_dict[action])

root.bind('<Key>', on_key_press)


while game_not_started:
    startTime = time()
    animate_background()
    endTime = time()
    elapsedTime = endTime - startTime
    print(1.0/elapsedTime)
