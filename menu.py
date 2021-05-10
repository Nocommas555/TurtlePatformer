from tkinter import *
import tkinter.font as tkfont
import os
from test import start_level

root = Tk()
sets = {
    "sound": False,
    "jump": "w",
    "duck": "s",
    "run_right": "d",
    "run_left": "a",
    "force": "e"
    }

def change_menu(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack()
    root.update()

def load_game(parent_frame):
  parent_frame.pack_forget()
  start_level(root)

def flip_sound_setting():
    global sets
    if (sets["sound"]):
        Label(master = settings, text = 'ON', font = regular_font, bg = '#238823')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)
    else:
        Label(master = settings, text = 'OFF', font = regular_font, bg = '#D2222D')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)

    sets["sound"] = not sets["sound"]


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

Button(master = settings,
       text = 'Sound',
       font = regular_font,
       command = lambda: flip_sound_setting()
    ).place(relx = 0.48, rely = 0.2,
            width = 200, height = 50,
            anchor = CENTER)

Button(master = settings,
       text = 'Some more option',
       font = regular_font,
       command = lambda: print("Spanish inquisition")
    ).place(relx = 0.5, rely = 0.3,
            width = 350, height = 50,
            anchor = CENTER)

Button(master = settings,
       text = 'Some more option, but lower',
       font = regular_font,
       command = lambda: print("lol")
    ).place(relx = 0.5, rely = 0.4,
            width = 350, height = 50,
            anchor = CENTER)

Button(master = settings,
       text = 'This button does nothing',
       font = regular_font,
       command = lambda: print("what did you expect?")
    ).place(relx = 0.5, rely = 0.5,
            width = 350, height = 50,
            anchor = CENTER)


Button(master = settings,
       text = 'Return to main menu',
       font = regular_font,
       command = lambda: change_menu(settings, main_menu)
    ).place(relx = 0.5, rely = 0.85,
            width = 300, height = 50,
            anchor = CENTER)

looking_for_change = False

jump_label = Label(master = settings,
      text = sets["jump"],
      font = regular_font,
      ).place(relx = 0.2, rely = 0.2, width = 100, height = 50, anchor = CENTER)

def on_key_press(event):
    global looking_for_change, jump_label
    if (looking_for_change):
        print(event.keysym)
        looking_for_change = False
        #jump_label.text = event.keysym
        #jump_label.configure(text = event.keysym)
        print(jump_label)
    else:
        return

root.bind("<Key>", on_key_press)

def change_state():
    global looking_for_change
    looking_for_change = not looking_for_change

Button(master = settings,
       text = 'Jump',
       font = regular_font,
       command = lambda: change_state()
    ).place(relx = 0.15, rely = 0.2,
            width = 100, height = 50,
            anchor = CENTER)




settings.pack()

settings.pack_forget()

#main_menu.tkraise()
root.mainloop()