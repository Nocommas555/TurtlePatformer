'''Tool for drawing colliders onto sprites and autogenerating img_descr.json'''
import json
import os
import tkinter as tk

# init globals
sprite_names = []
sprites = []
sprites_resized = []
target_sprite = 0
sprite_tk_image = None
sprite_scale = 1

colliders = []
curr_collider_id = 0

collider_types = [["rigid", "#bb0000"], ["trigger", "#00bb00"]]
draw_collider_type = 0

drawing = False
curr_collider_rect = None

# set up screen
root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=500)
canvas.pack()

def start_draw(event):
    '''starts collider drawing process'''
    global drawing, curr_collider_id
    drawing = True
    curr_collider_id = len(colliders)
    colliders.append({"x":event.x, "y":event.y})

def on_mouse_move(event):
    '''updates drawn box based on mouse position'''
    global curr_collider_rect
    if not drawing:
        return

    if curr_collider_rect is not None:
        canvas.delete(curr_collider_rect)

    x = colliders[curr_collider_id]["x"]
    y = colliders[curr_collider_id]["y"]
    fill=collider_types[draw_collider_type][1]
    curr_collider_rect = canvas.create_rectangle(x, y, event.x, event.y, outline="#000000", fill=fill, stipple="gray50")

def on_draw_finish(event):
    '''writes the drawn collider to global in img_descr format. Called on mouse up'''
    global drawing, curr_collider_rect
    colliders[curr_collider_id]["width"] = event.x - colliders[curr_collider_id]["x"]
    colliders[curr_collider_id]["height"] =  event.y - colliders[curr_collider_id]["y"]
    colliders[curr_collider_id]["x"] -= 500-int(sprites_resized[target_sprite].width()/2)
    colliders[curr_collider_id]["y"] -= 250-int(sprites_resized[target_sprite].height()/2)
    colliders[curr_collider_id]["type"] = collider_types[draw_collider_type][0]
    curr_collider_rect = None
    drawing = False

def load_sprites(path="./sprites"):
    '''loads images from a directory into memory'''
    global sprites, sprites_resized, sprite_names
    sprites = []
    sprites_resized = []
    sprite_names = os.listdir(path)
    for filename in sprite_names:
        sprites.append(tk.PhotoImage(file=path+"/"+filename))

    for sprite in sprites:
        sprites_resized.append(sprite)

    open_sprite(0, noclear=True)

def save_to_img_descr(collider_base_name="collider"):
    '''saves global collider information to img_descr file'''
    #create if doesn't exist, then read
    open("img_descr.json", "a+")
    with open("img_descr.json", "r") as img_descr:

        try:
            data = json.load(img_descr)
        except:
            # no valid json in the file
            data = {"images":{}}

        data["images"][sprite_names[target_sprite]] = {"hitboxes":{}, "extra":{}, "scale":sprite_scale}
        for i, collider in enumerate(colliders):
            data["images"][sprite_names[target_sprite]]["hitboxes"][collider_base_name+"_"+str(i+1)] = collider

    with open("img_descr.json", "w+") as img_descr:
        json.dump(data, img_descr, indent=4, sort_keys=True)

def load_from_img_descr():
    '''loads data from img_descr to global colliders'''
    open("img_descr.json", "a+")

    try:
        img_descr_data = json.load(open("img_descr.json", "r"))
        return list(img_descr_data["images"][sprite_names[target_sprite]]["hitboxes"].values())
    except:
        # no valid json in the file
        return []

def open_sprite(index = 0, scale = None, noclear = False):
    '''selects the sprite at index to be active'''
    global sprite_tk_image, target_sprite, colliders

    if not noclear:
        save_to_img_descr()

    if scale is None:
        scale = sprite_scale

    index = index % len(sprites)
    target_sprite = index

    canvas.delete("all")

    if scale > 0:
        sprites_resized[index] = sprites[index].zoom(scale)

    sprite_tk_image = canvas.create_image(500, 250, image=sprites_resized[index])

    colliders = load_from_img_descr()

    for collider in colliders:
        collider_x = 500-int(sprites_resized[target_sprite].width()/2) + collider["x"]
        collider_y = 250-int(sprites_resized[target_sprite].height()/2) + collider["y"]

        color = "#000000"
        for collider_type in collider_types:
            if collider_type[0] == collider["type"]:
                color = collider_type[1]

        x = collider_x
        y = collider_y
        x2 = collider_x+collider["width"]
        y2 = collider_y+collider["height"]
        canvas.create_rectangle(x, y, x2, y2, outline="#000000", fill=color, stipple="gray50")

def size_up():
    '''increases sprite scale'''
    global sprite_scale
    sprite_scale += 1
    open_sprite(target_sprite)

def size_down():
    '''decreases sprite scale'''
    global sprite_scale
    if sprite_scale > 1:
        sprite_scale -= 1
        open_sprite(target_sprite)

def cycle_collider_type():
    '''chages current collider type'''
    global draw_collider_type
    draw_collider_type = (draw_collider_type+1)%len(collider_types)

def reset():
    '''deletes all colliders for active sprite'''
    global colliders
    colliders = []

    open_sprite(target_sprite)

# set up UI

control_panel = tk.Frame(root, width = 1000, height = 200, bg = '#000000')

tk.Button(
    master=control_panel,
    text="Next Sprite",
    command=lambda: open_sprite(target_sprite+1))\
        .place(relx=0.25, rely=0.25, relwidth=0.2, relheight=0.3, anchor="center")

tk.Button(
    master=control_panel,
    text="Prev Sprite",
    command=lambda: open_sprite(target_sprite-1))\
        .place(relx=0.25, rely=0.7, relwidth=0.2, relheight=0.3, anchor="center")

tk.Button(
    master=control_panel,
    text="Size Up", command=size_up)\
        .place(relx=0.5, rely=0.25, relwidth=0.2, relheight=0.3, anchor="center")

tk.Button(
    master=control_panel,
    text="Size Down",
    command=size_down)\
        .place(relx=0.5, rely=0.7, relwidth=0.2, relheight=0.3, anchor="center")

tk.Button(
    master=control_panel,
    text="Change Collider Type",
    command=cycle_collider_type)\
        .place(relx=0.75, rely=0.25, relwidth=0.2, relheight=0.3, anchor="center")

tk.Button(
    master=control_panel,
    text="Undo", command=reset)\
        .place(relx=0.75, rely=0.7, relwidth=0.2, relheight=0.3, anchor="center")

control_panel.pack()

canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_draw_finish)

load_sprites()

root.mainloop()
