from tkinter import *
import tkinter.font as tkfont
import os
import json
from test import start_level

root = Tk()
sets = {
    "sound": False,
    "jump": "w",
    "duck": "s",
    "run_right": "d",
    "run_left": "a",
    "force": "e",
    "atack": "space"
    }

def load_settings():
    global sets
    open("settings.json", "a+")
    sets = json.load(open("settings.json"))

def save_settings():
    global sets
    json.dump(sets, open("settings.json", "w"))

load_settings()


def change_menu(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack()
    root.update()

def load_game(parent_frame):
  parent_frame.pack_forget()
  start_level(root)

def flip_sound_setting():
    global sets

    sets["sound"] = not sets["sound"]
    save_settings()

    if (sets["sound"]):
        Label(master = settings, text = 'ON', font = regular_font, bg = '#238823')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)
    else:
        Label(master = settings, text = 'OFF', font = regular_font, bg = '#D2222D')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)



regular_font = tkfont.Font(family = 'Noto Sans', size = 16)
big_font = tkfont.Font(family = 'Noto Sans',size = 32)
title_font = tkfont.Font(family = 'Noto Sans Display', size = 40)

main_menu = Frame(root, width = 1600, height = 800, bg = '#033580')

Label(master = main_menu,
      text = 'THE GREAT ADVENTURE OF LUKE AND SKYWALKER',
      font = title_font,
      bg = '#033580',
      fg = '#d9d211'
      ).place(relx = 0.5, rely = 0.25, width = 1600, height = 300, anchor = CENTER)

Button(master = main_menu,
       text = 'Play',
       font = big_font,
       command = lambda: load_game(main_menu)
    ).place(relx = 0.5, rely = 0.6,
            width = 200, height = 100,
            anchor = CENTER)

Button(master = main_menu,
       text = 'Settings',
       font = regular_font,
       command = lambda: change_menu(main_menu, settings)
    ).place(relx = 0.5, rely = 0.75,
            width = 100, height = 50,
            anchor = CENTER)

Button(master = main_menu,
       text = 'Exit',
       font = regular_font,
       command = lambda: os._exit(0)
    ).place(relx = 0.5, rely = 0.85,
            width = 100, height = 50,
            anchor = CENTER)

settings = Frame(width = 1600, height = 800, bg = '#AAAAAA')
main_menu.pack()
flip_sound_setting()
flip_sound_setting()


Button(master = settings,
       text = 'Sound',
       font = regular_font,
       command = lambda: flip_sound_setting()
    ).place(relx = 0.48, rely = 0.2,
            width = 200, height = 50,
            anchor = CENTER)


Button(master = settings,
       text = 'Return to main menu',
       font = regular_font,
       command = lambda: change_menu(settings, main_menu)
    ).place(relx = 0.5, rely = 0.85,
            width = 300, height = 50,
            anchor = CENTER)

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

root.bind("<Key>", on_key_press)

def change_state_to(stat):
    global state
    state = stat

Button(master = settings,
       text = 'Jump',
       font = regular_font,
       command = lambda: change_state_to("jump")
    ).place(relx = 0.43, rely = 0.27,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["jump"] = Label(master = settings,
      text = sets["jump"],
      font = regular_font
      )
dic_label["jump"].place(relx = 0.53, rely = 0.27, width = 150, height = 50, anchor = CENTER)

Button(master = settings,
       text = 'Duck',
       font = regular_font,
       command = lambda: change_state_to("duck")
    ).place(relx = 0.43, rely = 0.34,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["duck"] = Label(master = settings,
      text = sets["duck"],
      font = regular_font
      )
dic_label["duck"].place(relx = 0.53, rely = 0.34, width = 150, height = 50, anchor = CENTER)

Button(master = settings,
       text = 'Move right',
       font = regular_font,
       command = lambda: change_state_to("run_right")
    ).place(relx = 0.43, rely = 0.41,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["run_right"] = Label(master = settings,
      text = sets["run_right"],
      font = regular_font
      )
dic_label["run_right"].place(relx = 0.53, rely = 0.41, width = 150, height = 50, anchor = CENTER)

Button(master = settings,
       text = 'Move left',
       font = regular_font,
       command = lambda: change_state_to("run_left")
    ).place(relx = 0.43, rely = 0.48,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["run_left"] = Label(master = settings,
      text = sets["run_left"],
      font = regular_font
      )
dic_label["run_left"].place(relx = 0.53, rely = 0.48, width = 150, height = 50, anchor = CENTER)

Button(master = settings,
       text = 'Use force',
       font = regular_font,
       command = lambda: change_state_to("force")
    ).place(relx = 0.43, rely = 0.55,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["force"] = Label(master = settings,
      text = sets["force"],
      font = regular_font
      )
dic_label["force"].place(relx = 0.53, rely = 0.55, width = 150, height = 50, anchor = CENTER)

Button(master = settings,
       text = "Byty kohos'",
       font = regular_font,
       command = lambda: change_state_to("atack")
    ).place(relx = 0.43, rely = 0.62,
            width = 150, height = 50,
            anchor = CENTER)

dic_label["atack"] = Label(master = settings,
      text = sets["atack"],
      font = regular_font
      )
dic_label["atack"].place(relx = 0.53, rely = 0.62, width = 150, height = 50, anchor = CENTER)




settings.pack()

settings.pack_forget()

#main_menu.tkraise()
root.mainloop()