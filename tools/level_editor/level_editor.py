''' Tool, used to create levels
    from pre-made sprites, building blocks in this context'''
import json
import os
import tkinter as tk


# init globals
sprite_names = []
sprites_pictures = {}
sprites_pictures_scales = {}
current_sprite_name = None
shadow = None
level_data = []
changes = []
camera_offset_x = 0
camera_offset_y = 0
drag_point = {}
movable_state = False


# set up screen
root = tk.Tk()
root.geometry("1600x800")

canvas = tk.Canvas(root, bg="#696969")
canvas.pack(side=tk.LEFT,  fill=tk.BOTH, expand=1)


# main functional
def load_sprites(path="../../sprites"):
    ''' Loads sprites from a given folder '''
    global sprites_pictures, sprites_pictures_scales, sprite_names

    sprite_names = os.listdir(path)
    #open(path+"/"+"img_descr.json", "a+")

    try:
        img_descr_data = json.load(open(path+"/"+"img_descr.json", "r"))
    except Exception:
        img_descr_data = {}

    for filename in list(sprite_names):
        if ".png" in filename:
            if "scale" in img_descr_data["images"][filename]:
                scale = img_descr_data["images"][filename]["scale"]
            else:
                scale = 1
            sprites_pictures[filename] = tk.PhotoImage(
                file=path+"/"+filename
            ).zoom(scale)
        else:
            sprite_names.remove(filename)
load_sprites()

def save_to_file(filename="level.json"):
    ''' Saves level to a .json file '''
    global level_data

    open(filename, "a+")
    with open(filename, "w+") as level_file:
        json.dump(level_data, level_file)

def get_additional_settings():
    ''' Gets string which user inputs
        into a special field (entry_widget) '''

    global entry_widget

    try:
        return json.loads(entry_widget.get())
    except Exception:
        return {}


def update_camera(displacement_x, displacement_y):
    ''' Moves camera given number of pixels '''
    canvas.move("all", displacement_x, displacement_y)

def start_camera_drag(event):
    ''' Remembers where we start draging our camera '''
    global drag_point

    drag_point = {"x": event.x, "y": event.y}

def drag_camera(event):
    ''' Continuosly moves camera with mouse '''
    global drag_point, camera_offset_x, camera_offset_y

    camera_offset_x += event.x - drag_point["x"]
    camera_offset_y += event.y - drag_point["y"]

    update_camera(event.x-drag_point["x"], event.y-drag_point["y"])

    drag_point = {"x": event.x, "y": event.y}


def on_mouse_click(event):
    ''' Adds new element to level
        and draws it on canvas '''
    global sprites_pictures, sprites_pictures_scales,\
        current_sprite_name, entry_widget, changes

    print(
        "clicked at",
        event.x-camera_offset_x,
        event.y-camera_offset_y
    )
    changes.append(
        canvas.create_image(
            event.x,
            event.y,
            image=sprites_pictures[current_sprite_name],
            anchor=tk.NW
        )
    )
    if movable_state:
        phys_type = "movable"
    else:
        phys_type = "immovable"
    level_data.append({
        "x": event.x - camera_offset_x,
        "y": event.y - camera_offset_y,
        "filename": current_sprite_name,
        "phys_type": phys_type,
        "additional": get_additional_settings()
    })
    save_to_file()

def on_mouse_move(event):
    ''' Redraws preview of the current
        selected building block, called shadow '''
    global current_sprite_name, shadow, sprites_pictures_scales

    if not current_sprite_name:
        return

    if shadow:
        canvas.delete(shadow)
    shadow = canvas.create_image(
        event.x,
        event.y,
        image=sprites_pictures[current_sprite_name],
        anchor=tk.NW
    )

def undo(event):
    ''' Called on right mouse click,
        undoes last change'''
    global changes, level_data

    canvas.delete(changes.pop())
    level_data.pop()
    save_to_file()

def update_selection(event):
    ''' Changes current selected building block '''
    global current_sprite_name

    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        current_sprite_name = event.widget.get(index)
    return current_sprite_name

def change_phys_state():
    ''' Is our building block movable or static?
        Anyway, we`ve changed it`s state to opposite'''
    global movable_state

    movable_state = not movable_state
    print("movable_state changed to", movable_state)


# set up UI
toolbar_frame = tk.Frame(root)
picture_select_frame = tk.Frame(toolbar_frame)

scrollbar = tk.Scrollbar(picture_select_frame)
my_list = tk.Listbox(picture_select_frame, yscrollcommand=scrollbar.set)
for filename in sprite_names:
    my_list.insert(tk.END, str(filename))
scrollbar.config(command=my_list.yview)

entry_widget = tk.Entry(toolbar_frame)

change_state_check = tk.Checkbutton(
    toolbar_frame,
    text='Movable',
    command=change_phys_state
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
my_list.pack(side=tk.LEFT, fill=tk.BOTH)
picture_select_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
entry_widget.pack(side=tk.BOTTOM, fill=tk.BOTH)
change_state_check.pack(side=tk.BOTTOM, fill=tk.X)
toolbar_frame.pack(side=tk.RIGHT, fill=tk.Y)


canvas.bind("<Button-1>", on_mouse_click)
canvas.bind("<Motion>", on_mouse_move)
canvas.bind('<Button-3>', undo)
my_list.bind("<<ListboxSelect>>", update_selection)
canvas.bind("<Button-2>", start_camera_drag)
canvas.bind("<B2-Motion>", drag_camera)


root.mainloop()
