import tkinter as tk
import tkinter.font as tkfont
import os
import json
from test import start_level
from Chelone import SpriteLoader
import time
import math

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
time_elapsed = 0
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

# declare classes
class Sprite:
    def __init__(
        self,
        ID="?",
        x=0,
        y=0,
        width=0,
        height=0,
        anchor=tk.NW,
        img_file=None,
        parent_frame=None
    ):
        self.ID = ID
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = tk.PhotoImage(file=img_file)
        self.instance = parent_frame.create_image(
            self.x,
            self.y,
            anchor=anchor,
            image=self.image
        )
        self.parent_frame=parent_frame
        self.last_movement_x = 0
        self.last_movement_y = 0

    def on_click(self, offset_x, offset_y):
        pass

    def move(self, dx, dy):
        self.parent_frame.move(self.instance, dx, dy)
        self.x += dx
        self.y += dy
        self.last_movement_x = dx
        self.last_movement_y = dy

class DragableSprite(Sprite):
    def on_click(self, offset_x, offset_y):
        global current_drag_sprite

        self.drag_point = {"x": offset_x, "y": offset_y}

        current_drag_sprite = self

class PlayButton(Sprite):
    def on_click(self, offset_x, offset_y):
        main_menu.pack_forget()
        start_level(root)

class SettingsButton(Sprite):
    def on_click(self, offset_x, offset_y):
        change_frame(main_menu, settings_frame)

class ExitButton(Sprite):
    def on_click(self, offset_x, offset_y):
        os._exit(0)

# set up screen
root = tk.Tk()
root.geometry("1600x800")

main_menu = tk.Canvas(root, bg="#000000")
main_menu.pack(fill=tk.BOTH, expand=1)

settings_frame =\
    tk.Frame(root, width = 1600, height = 800, bg = '#002550')

b_background =\
    tk.PhotoImage(file="./menu_pics/b_background.png")
b_background_instance =\
    main_menu.create_image(0, 0, image=b_background, anchor=tk.NW)
b_background_instance_next =\
    main_menu.create_image(1300, 0, image=b_background, anchor=tk.NW)

my_objects.append(
    DragableSprite(
        ID="b_planet_r",
        x=80,
        y=500,
        width=65,
        height=97,
        img_file="./menu_pics/b_planet_ring.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    DragableSprite(
        ID="b_planet",
        x=1100,
        y=50,
        width=57,
        height=57,
        img_file="./menu_pics/b_planet.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    DragableSprite(
        ID="b_death_star",
        x=1400,
        y=480,
        width=176,
        height=176,
        img_file="./menu_pics/b_death_star.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    Sprite(
        ID="f_title",
        x=10,
        y=230,
        img_file="./menu_pics/1_title_image.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    PlayButton(
        ID="m_play",
        x=684,
        y=480,
        width=228,
        height=100,
        img_file="./menu_pics/m_play.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    SettingsButton(
        ID="m_settings",
        x=715,
        y=600,
        width=169,
        height=50,
        img_file="./menu_pics/m_settings.png",
        parent_frame=main_menu
    )
)
my_objects.append(
    ExitButton(
        ID="m_exit",
        x=750,
        y=680,
        width=100,
        height=50,
        img_file="./menu_pics/m_exit.png",
        parent_frame=main_menu
    )
)

my_objects.reverse()

regular_font = tkfont.Font(family = 'Noto Sans Display', size = 16)


# main functional
def load_settings():
    global user_settings

    open("settings.json", "a+")
    try:
        user_settings = json.load(open("settings.json"))
    except Exception as e:
        pass

def save_settings():
    global user_settings

    # create file if not found
    open("settings.json", "a+")
    json.dump(user_settings, open("settings.json", "w"))


def change_frame(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack(fill=tk.BOTH, expand=1)
    root.update()

def press_button_main_menu(event):
    global my_objects

    for obj in my_objects:
        if obj.x < event.x < obj.x + obj.width\
        and obj.y < event.y < obj.y + obj.height:
            print("e")
            obj.on_click(obj.x - event.x,obj.y - event.y)

def drag_sprite(event):
    global my_objects

    for obj in my_objects:
        if isinstance(obj, DragableSprite):
            if obj is current_drag_sprite:
                obj.move(
                    event.x + obj.drag_point["x"] - obj.x,
                    event.y + obj.drag_point["y"] - obj.y
                )
                print(obj.last_movement_x, obj.last_movement_y)

def release_sprite(event):
    global current_drag_sprite

    current_drag_sprite = None

def flip_sound_setting():
    global user_settings

    user_settings["sound"] = not user_settings["sound"]

    on_label = tk.Label(
        master=settings_frame,
        text='ON',
        font=regular_font,
        fg='#111111',
        bg='#238823'
    )
    off_label = tk.Label(
        master = settings_frame,
        text = 'OFF',
        font = regular_font,
        fg='#111111',
        bg = '#D2222D'
    )

    if (user_settings["sound"]):
        sound_label = on_label
    else:
        sound_label = off_label

    sound_label.place(
        relx = 0.544,
        rely = 0.13,
        width = 50,
        height = 50
    )

    save_settings()

def on_key_press(event):
    global state, states_label

    if (state != ""):
        states_label[state].configure(text = event.keysym)
        user_settings[state] = event.keysym
        state = ""
        save_settings()
    else:
        return

def change_state_to(state_parameter):
    global state

    state = state_parameter

def add_button_with_label(
    master=settings_frame,
    text="?",
    font=regular_font,
    foreground="#000000",
    command=None,
    relx=0.5,
    rely=0.5,
    button_width=150,
    button_height=50,
    label_width=150,
    label_height=50,
    anchor=tk.CENTER,
    ID="unnamed"
):
    tk.Button(
        master=master,
        text=text,
        font=font,
        fg=foreground,
        command=command
    ).place(
        relx=relx,
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
        relx=relx*1.01 + (button_width/1600),
        rely=rely*1.01,
        width=label_width,
        height=label_height,
        anchor=anchor
    )

def animate_background():
    global b_background_instance, b_background_instance_next, time_elapsed

    time.sleep(0.001)
    time_elapsed += 1
    if time_elapsed % 10 == 0:
        main_menu.move(b_background_instance, -1, 0)
        main_menu.move(b_background_instance_next, -1, 0)
    if time_elapsed >= 13000:
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
        time_elapsed = 0
    for obj in my_objects:
        if obj is not current_drag_sprite:
            obj.last_movement_x
            obj.last_movement_y
            obj.move(obj.last_movement_x, obj.last_movement_y)
    root.update()

# set up settings UI
tk.Button(
    master=settings_frame,
    text='Sound',
    font=regular_font,
    fg="#000000",
    command=lambda:flip_sound_setting()
).place(
    relx=0.382,
    rely=0.13,
    width=250,
    height=50
)
tk.Button(
    master=settings_frame,
    text='Return to main menu',
    font=regular_font,
    fg="#000000",
    command=lambda:change_frame(settings_frame, main_menu)
).place(
    relx=0.382,
    rely=0.75,
    width=300,
    height=50
)
add_button_with_label(
    text="Jump",
    command=lambda:change_state_to("jump"),
    relx=0.43,
    rely=0.27,
    ID="jump"
)
add_button_with_label(
    text="Duck",
    command=lambda:change_state_to("duck"),
    relx=0.43,
    rely=0.34,
    ID="duck"
)
add_button_with_label(
    text="Move right",
    command=lambda:change_state_to("run_right"),
    relx=0.43,
    rely=0.41,
    ID="run_right"
)
add_button_with_label(
    text="Move left",
    command=lambda:change_state_to("run_left"),
    relx=0.43,
    rely=0.48,
    ID="run_left"
)
add_button_with_label(
    text="Use force",
    command=lambda:change_state_to("force"),
    relx=0.43,
    rely=0.55,
    ID="force"
)
add_button_with_label(
    text="Byty kohos'",
    command=lambda:change_state_to("atack"),
    relx=0.43,
    rely=0.62,
    ID="atack"
)


# make some preparations
load_settings()
flip_sound_setting()
flip_sound_setting()


root.bind("<Key>", on_key_press)
main_menu.bind("<Button-1>", press_button_main_menu)
main_menu.bind("<B1-Motion>", drag_sprite)
main_menu.bind("<B1-ButtonRelease>", release_sprite)


while 1:
    animate_background()