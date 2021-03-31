 #plays file via vlc
def _playsoundLinux(sound):
	import os
	os.system('cvlc ' + sound)

from platform import system
system = system()
print(system)

if system == 'Linux':
	playsound = _playsoundLinux

del system

#test
playsound('/home/vlad/Desktop/sound/file_example_MP3_1MG.mp3')