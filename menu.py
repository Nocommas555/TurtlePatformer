from tkinter import *
import tkinter.font as tkfont
import os
from test import start_level

root = Tk()

def change_menu(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack()
    root.update()

def load_game(parent_frame):
  parent_frame.pack_forget()
  start_level(root)

sound_enabled = False
def flip_sound_setting():
    global sound_enabled
    if (sound_enabled):
        Label(master = settings, text = 'ON', font = regular_font, bg = '#238823')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)
    else:
        Label(master = settings, text = 'OFF', font = regular_font, bg = '#D2222D')\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)

    sound_enabled = not sound_enabled


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

#Button(master = main_menu, text='Settings', command=lambda:change_menu(main_menu, settings)).place(relx = 0.5, rely = 0.2, width = 100, height = 50, anchor = CENTER)
#Button(master = main_menu, text='Exit', command=lambda:change_menu(main_menu, settings)).place(relx = 0.5, rely = 0.3, width = 100, height = 50, anchor = CENTER)

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

settings.pack()

settings.pack_forget()

#main_menu.tkraise()
root.mainloop()