## TurtlePlatformer

<img align="center" alt="Title" width="100%" src="readme/title.png" />

Basic platformer written on a custom engine using tkinter as a graphics library

## Demonstration of our engine
---
<img align="center" alt="Menu" width="100%" src="readme/menu.png" />

---
This is main menu. It have buttons like this:
- Exit button. Allows user to close our program;
- Settings button. Allows user to set up his game process;
- Play button. Runs test.py and generates level.
---
<img align="center" alt="Settings" width="100%" src="readme/sets.png" />

---
This is settings menu. In this tab you can change your key bindings and turn on/off sound.

---

## Below you can see screenshots of game process
---
<img align="center" alt="Game1" width="100%" src="readme/game1.png" />

---
<img align="center" alt="Game2" width="100%" src="readme/game2.png" />

---
<img align="center" alt="Game3" width="100%" src="readme/game3.png" />

---

## Currently implemented engine features:

## _Renderer_
---
- supports sprite layering
- implements basic camera functionality
---
## _Phys engine_
---
- basic collision detection and handling using square hitboxes
- velocities and gravity simulation
- allows user to use multithreading
---
## _Picture and animation loader_
---
- can be instantiated multiple times to allow for unloading only some assets. (e.g one instance for the player that does not get unloaded between levels)
- caches all pictures and their descriptors
---
## _Sound engine_
---
- a basic winapi wrapper to play mp3's and wav sounds
- used since python has no built-in music lib
---
## _Collider_drawer_
---
- a tool to draw colliders

## Contributors

- Oleg Shkurenko(nocommas555)
- Vladyslav Kravchenko(cyberlord-coder-228)
- Kyrylo Cholombytko(1mperix)

## Special thanks

- Timur Shemsedinov