from tkinter import *
import tkinter.font as tkfont

def change_menu(this_frame, next_frame):
    this_frame.pack_forget()
    next_frame.pack()

root = Tk()

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
       command = lambda: print("Not ready yet, enjoy this beautiful menu")
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
       command = lambda: print("Please, close this window yourself by pressing X in the top right corner")
    ).place(relx = 0.5, rely = 0.85,
            width = 100, height = 50,
            anchor = CENTER)

#Button(master = main_menu, text='Settings', command=lambda:change_menu(main_menu, settings)).place(relx = 0.5, rely = 0.2, width = 100, height = 50, anchor = CENTER)
#Button(master = main_menu, text='Exit', command=lambda:change_menu(main_menu, settings)).place(relx = 0.5, rely = 0.3, width = 100, height = 50, anchor = CENTER)

settings = Frame(width = 1600, height = 800, bg = '#5e6969')
main_menu.pack()

def set_sound_to(sound_status = "off"):
    if (sound_status == 'off'):
        Label(master = settings, text = 'OFF', font = regular_font)\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)
    else:
        Label(master = settings, text = 'ON', font = regular_font)\
            .place(relx = 0.57, rely = 0.2, width = 50, height = 50, anchor = CENTER)

set_sound_to('off')
sound_status = 'off'

def change_sound():
    global sound_status
    if(sound_status == 'off'):
        sound_status = 'on'
        set_sound_to('on')
    else:
        sound_status = 'off'
        set_sound_to('off')


Button(master = settings,
       text = 'Sound',
       font = regular_font,
       command = lambda: change_sound()
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