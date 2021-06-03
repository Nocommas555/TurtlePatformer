''' Our main menu + settings menu '''

import tkinter as tk
import tkinter.font as tkfont
import os
import json
from test import start_level
from time import time, sleep
import functools


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
frames_lapsed = 0
state = ""
states_label = {
    "sound": False,
    "jump": None,
    "duck": None,
    "run_right": None,
    "run_left": None,
    "force": None,
    "atack": None
}
my_objects = []
drag_point = {}
current_drag_sprite = None
picture_parent_directory = './menu_pics/'
settings_file_name = 'settings.json'
game_not_started = True
window_width = 1600
window_height = 800
background_width = 2600

TARGET_FPS = 30
frame_period = 1.0/TARGET_FPS
now = time()
next_frame_time = now + frame_period

# declare classes
class Sprite:
    ''' Pictures on the main screen '''
    anchor_offsets = {
        tk.CENTER: {'x': -0.5, 'y': -0.5},
        tk.NW: {'x': 0, 'y': 0},
        tk.SW: {'x': 0, 'y': -1},
        tk.NE: {'x': -1, 'y': 0},
        tk.SE: {'x': -1, 'y': -1}
    }

    def __init__(
        self, ID="?",x=0, y=0, width=0, height=0,
        anchor=tk.NW, img_file=None, parent_frame=None
    ):
        self.ID = ID
        self.x = x + width * self.anchor_offsets[anchor]['x']
        self.y = y + height * self.anchor_offsets[anchor]['y']
        self.width = width
        self.height = height
        self.image = tk.PhotoImage(file=img_file)
        self.instance = parent_frame.create_image(
            x, y,
            anchor=anchor,
            image=self.image
        )
        self.parent_frame=parent_frame
        self.last_movement_x = 0
        self.last_movement_y = 0

    def on_click(self, offset_x, offset_y):
        ''' Might be overriden '''
        pass # noqa , function meant to be extended

    def move(self, dx, dy):
        ''' Moves sprite if needed '''
        self.parent_frame.move(self.instance, dx, dy)
        self.x += dx
        self.y += dy
        self.last_movement_x = dx
        self.last_movement_y = dy

class DragableSprite(Sprite):
    ''' Sprites which you can move with mouse '''
    def on_click(self, offset_x, offset_y):
        global current_drag_sprite

        self.drag_point = {"x": offset_x, "y": offset_y}

        current_drag_sprite = self

class PlayButton(Sprite):
    ''' Button that starts level '''
    def on_click(self, offset_x, offset_y):
        global game_not_started

        main_menu.pack_forget()
        game_not_started = False
        start_level(root)

class SettingsButton(Sprite):
    ''' Button that sends you to settings menu '''
    def on_click(self, offset_x, offset_y):
        change_frame(main_menu, settings_frame)

class ExitButton(Sprite):
    ''' Button that exits program '''
    def on_click(self, offset_x, offset_y):
        os._exit(0) # noqa , only way to kill child processes


# set up screen
root = tk.Tk()
root.geometry(str(window_width)+'x'+str(window_height))

main_menu = tk.Canvas(root, bg="black")
main_menu.pack(fill=tk.BOTH, expand=1)

settings_frame =\
    tk.Frame(root, width=window_width, height=window_height, bg="black")

b_background =\
    tk.PhotoImage(file=picture_parent_directory+"b_background.png")
b_background_instance =\
    main_menu.create_image(0, 0, image=b_background, anchor=tk.NW)
b_background_instance_next =\
    main_menu.create_image(background_width/2, 0, image=b_background, anchor=tk.NW)

my_objects.append(
    DragableSprite(
        x=80,
        y=500,
        width=65,
        height=97,
        img_file=picture_parent_directory+"b_planet_ring.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    DragableSprite(
        x=1100,
        y=50,
        width=57,
        height=57,
        img_file=picture_parent_directory+"b_planet.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    DragableSprite(
        x=1400,
        y=480,
        width=176,
        height=176,
        img_file=picture_parent_directory+"b_death_star.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    Sprite(
        x=10,
        y=230,
        img_file=picture_parent_directory+"1_title_image.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    PlayButton(
        x=window_width*0.5,
        y=480,
        width=228,
        height=100,
        img_file=picture_parent_directory+"m_play.png",
        parent_frame=main_menu,
        anchor=tk.CENTER
    )
)
my_objects.append(
    SettingsButton(
        x=715,
        y=600,
        width=169,
        height=50,
        img_file=picture_parent_directory+"m_settings.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    ExitButton(
        x=750,
        y=680,
        width=100,
        height=50,
        img_file=picture_parent_directory+"m_exit.png",
        parent_frame=main_menu
    )
)

# reverse order of objects,
# so that ones which are on top have higher interaction priority
my_objects.reverse()

regular_font = tkfont.Font(family='Noto Sans Display', size=16)


# main functional
def load_settings():
    ''' Loads settings '''
    global user_settings

    open(settings_file_name, "a+")
    try:
        user_settings = json.load(open(settings_file_name))
    except:
        pass

def save_settings():
    ''' Saves settings '''
    global user_settings

    # create file if not found
    open(settings_file_name, "a+")

    json.dump(user_settings, open(settings_file_name, "w"))


def change_frame(this_frame, next_frame):
    ''' Changes frame '''
    this_frame.pack_forget()
    next_frame.pack(fill=tk.BOTH, expand=1)
    root.update()

def press_button_main_menu(event):
    ''' Detects if user clicked on sprite in main menu '''
    for obj in my_objects:
        if obj.x < event.x < obj.x + obj.width\
        and obj.y < event.y < obj.y + obj.height:
            print("e")
            obj.on_click(obj.x - event.x,obj.y - event.y)

def drag_sprite(event):
    ''' Moves movable sprite while mouse clicked and moving '''
    for obj in my_objects:
        if isinstance(obj, DragableSprite):
            if obj is current_drag_sprite:
                obj.move(
                    event.x + obj.drag_point["x"] - obj.x,
                    event.y + obj.drag_point["y"] - obj.y
                )
                print(obj.last_movement_x, obj.last_movement_y)

def release_sprite(event): # noqa , parameter event needed for callback signature
    ''' Stops current movable sprite from moving when unclicked'''
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
        width=window_width*0.07,
        height=window_height*0.07,
        anchor=tk.CENTER
    )

    save_settings()

def on_key_press(event):
    ''' Reasignes control key of a selected action '''
    global state, states_label

    if state != "":
        states_label[state].configure(text=event.keysym)
        user_settings[state] = event.keysym
        state = ""
        save_settings()
    else:
        return

def change_state_to(state_parameter):
    ''' Detects which action is changes control key '''
    global state

    state = state_parameter

def add_button_with_label(
    master=settings_frame,
    text="?",
    font=regular_font,
    foreground="blue",
    command=None,
    function_arguments=(),
    relx=0.5,
    rely=0.5,
    button_width=150,
    button_height=50,
    label_width=150,
    label_height=50,
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
        relx=relx-button_width/window_width/2,
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
        relx=relx*1.01+button_width/window_width/2,
        rely=rely*1.01,
        width=label_width,
        height=label_height,
        anchor=anchor
    )

def restart_fps_timer():
    ''' Resets the variables associated with fps waiting '''
    global frame_period, TARGET_FPS, now, next_frame_time

    frame_period = 1.0/TARGET_FPS
    now = time()
    next_frame_time = now + frame_period

def animate_background():
    ''' Animates stars and palnets on the background '''
    global b_background_instance, b_background_instance_next,\
        frames_lapsed, frame_period, TARGET_FPS, now, next_frame_time

    now = time()
    while now < next_frame_time:
        sleep(next_frame_time - now)
        now = time()

    next_frame_time = now + frame_period

    frames_lapsed += 1

    main_menu.move(b_background_instance, -1, 0)
    main_menu.move(b_background_instance_next, -1, 0)

    if frames_lapsed >= 1300:
        # kinda reset
        main_menu.delete(b_background_instance)
        b_background_instance = b_background_instance_next
        b_background_instance_next = main_menu.create_image(
            1300,
            0,
            image=b_background,
            anchor=tk.NW
        )
        main_menu.lower(b_background_instance_next)
        frames_lapsed = 0
    # inertia implentation
    for obj in my_objects:
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
    width=window_width*0.2,
    height=window_height*0.07,
    anchor=tk.CENTER
)

tk.Button(
    master=settings_frame,
    text='Return to main menu',
    font=regular_font,
    fg='blue',
    command=lambda:change_frame(settings_frame, main_menu)
).place(
    relx=0.5,
    rely=0.8,
    width=window_width*0.2,
    height=window_height*0.07,
    anchor=tk.CENTER
)

control_button_relx = 0.5
control_button_rely = 0.3
delta_rely = 0.07
for key in user_settings:
    if key == 'sound':
        continue

    add_button_with_label(
        text=key,
        command=change_state_to,
        function_arguments=(key),
        relx=control_button_relx,
        rely=control_button_rely,
        button_width=window_width*0.1,
        button_height=window_height*delta_rely*0.9,
        label_width=window_width*0.1,
        label_height=window_height*delta_rely*0.9,
        ID=key
    )
    control_button_rely += delta_rely

root.bind("<Key>", on_key_press)
main_menu.bind("<Button-1>", press_button_main_menu)
main_menu.bind("<B1-Motion>", drag_sprite)
main_menu.bind("<B1-ButtonRelease>", release_sprite)


while game_not_started:
    startTime = time()
    animate_background()
    endTime = time()
    elapsedTime = endTime - startTime
    print(1./elapsedTime)
