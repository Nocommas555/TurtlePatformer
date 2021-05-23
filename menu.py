import tkinter as tk
import tkinter.font as tkfont
import os
import json
from test import start_level

# init globals
state = ""
dic_label = {
    "sound": False,
    "jump": None,
    "duck": None,
    "run_right": None,
    "run_left": None,
    "force": None,
    "atack": None
}

# set default settings
sets = {
    "sound": False,
    "jump": "w",
    "duck": "s",
    "run_right": "d",
    "run_left": "a",
    "force": "e",
    "atack": "space"
}

# set up screen
root = tk.Tk()
root.geometry("1600x800")

main_menu = tk.Canvas(root, bg="#000000")
main_menu.pack(fill=tk.BOTH, expand=1)

b_background = tk.PhotoImage(file="./menu_pics/b_background.png")
b_planet_r = tk.PhotoImage(file="./menu_pics/b_planet_ring.png")
b_planet = tk.PhotoImage(file="./menu_pics/b_planet.png")
b_death_star = tk.PhotoImage(file="./menu_pics/b_death_star.png")
f_title = tk.PhotoImage(file="./menu_pics/1_title_image.png")
m_play = tk.PhotoImage(file="./menu_pics/m_play.png")
m_settings = tk.PhotoImage(file="./menu_pics/m_settings.png")
m_exit = tk.PhotoImage(file="./menu_pics/m_exit.png")

main_menu.create_image(0, 0, image=b_background, anchor=tk.NW)
main_menu.create_image(10, 200, image=f_title, anchor=tk.NW)
main_menu.create_image(80, 500, image=b_planet_r)
main_menu.create_image(1100, 50, image=b_planet)
main_menu.create_image(1400, 480, image=b_death_star)
main_menu.create_image(800, 480, image=m_play)
main_menu.create_image(800, 600, image=m_settings)
main_menu.create_image(800, 680, image=m_exit)

settings_frame = tk.Frame(width = 1600, height = 800, bg = '#003369')

regular_font = tkfont.Font(family = 'Noto Sans Display', size = 16)


# main functional
def load_settings():
    global sets

    open("settings.json", "a+")
    sets = json.load(open("settings.json"))

def save_settings():
    global sets

    json.dump(sets, open("settings.json", "w"))

def change_frame(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack(fill=tk.BOTH, expand=1)
    root.update()

def detect_click_main_menu(event):
    if event.x > 700 and event.x < 900 and event.y > 430 and event.y < 530:
        main_menu.pack_forget()
        start_level(root)
    if event.x > 750 and event.x < 850 and event.y > 575 and event.y < 625:
        main_menu.pack_forget()
        settings_frame.pack(fill=tk.BOTH, expand=1)
        root.update()
    if event.x > 750 and event.x < 850 and event.y > 655 and event.y < 705:
        os._exit(0)


def flip_sound_setting():
    global sets

    if (sets["sound"]):
        tk.Label(
            master = settings_frame,
            text = 'ON',
            font = regular_font,
            bg = '#238823'
        ).place(
            relx = 0.562,
            rely = 0.2,
            width = 50,
            height = 50,
            anchor = tk.CENTER
        )
    else:
        tk.Label(
            master = settings_frame,
            text = 'OFF',
            font = regular_font,
            bg = '#D2222D'
        ).place(
            relx = 0.562,
            rely = 0.2,
            width = 50,
            height = 50,
            anchor = tk.CENTER
        )


def on_key_press(event):
    global state, dic_label

    if (state != ""):
        #print(event.keysym)
        dic_label[state].configure(text = event.keysym)
        sets[state] = event.keysym
        #print(dic_label[state])
        state = ""
        save_settings()
    else:
        return

def change_state_to(state_parameter):
    global state

    state = state_parameter


# set up settings UI
tk.Button(
    master = settings_frame,
    text = 'Sound',
    font = regular_font,
    command = lambda: flip_sound_setting()
).place(
    relx = 0.461,
    rely = 0.2,
    width = 250,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Return to main menu',
    font = regular_font,
    command = lambda: change_frame(settings_frame, main_menu)
).place(
    relx = 0.5, rely = 0.85,
    width = 300, height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Jump',
    font = regular_font,
    command = lambda: change_state_to("jump")
).place(
    relx = 0.43,
    rely = 0.27,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)
dic_label["jump"] = tk.Label(
    master = settings_frame,
    text = sets["jump"],
    font = regular_font
)
dic_label["jump"].place(
    relx = 0.53,
    rely = 0.27,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Duck',
    font = regular_font,
    command = lambda: change_state_to("duck")
).place(relx = 0.43, rely = 0.34,
    width = 150, height = 50,
    anchor = tk.CENTER
)
dic_label["duck"] = tk.Label(
    master = settings_frame,
    text = sets["duck"],
    font = regular_font
)
dic_label["duck"].place(
    relx = 0.53, 
    rely = 0.34,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Move right',
    font = regular_font,
    command = lambda: change_state_to("run_right")
).place(
    relx = 0.43,
    rely = 0.41,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)
dic_label["run_right"] = tk.Label(
    master = settings_frame,
    text = sets["run_right"],
    font = regular_font
)
dic_label["run_right"].place(
    relx = 0.53,
    rely = 0.41,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Move left',
    font = regular_font,
    command = lambda: change_state_to("run_left")
).place(
    relx = 0.43,
    rely = 0.48,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)
dic_label["run_left"] = tk.Label(
    master = settings_frame,
    text = sets["run_left"],
    font = regular_font
)
dic_label["run_left"].place(
    relx = 0.53,
    rely = 0.48,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = 'Use force',
    font = regular_font,
    command = lambda: change_state_to("force")
).place(
    relx = 0.43,
    rely = 0.55,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)
dic_label["force"] = tk.Label(
    master = settings_frame,
    text = sets["force"],
    font = regular_font
)
dic_label["force"].place(
    relx = 0.53,
    rely = 0.55,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)

tk.Button(
    master = settings_frame,
    text = "Byty kohos'",
    font = regular_font,
    command = lambda: change_state_to("atack")
).place(
    relx = 0.43,
    rely = 0.62,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)
dic_label["atack"] = tk.Label(
    master = settings_frame,
    text = sets["atack"],
    font = regular_font
)
dic_label["atack"].place(
    relx = 0.53,
    rely = 0.62,
    width = 150,
    height = 50,
    anchor = tk.CENTER
)


load_settings()
flip_sound_setting()
flip_sound_setting()


root.bind("<Key>", on_key_press)
main_menu.bind("<Button-1>", detect_click_main_menu)

root.mainloop()