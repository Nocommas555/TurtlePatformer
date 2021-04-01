 #plays file via vlc

def _playsound_linux(file_source):
	import os
	os.system('cvlc ' + file_source)

def _playsound_crappy_win(file_source):
    import winsound
    winsound.PlaySound(file_source, winsound.SND_FILENAME)

from platform import system
system = system()
print(system)
if system == 'Linux':
	playsound = _playsound_linux
elif system == 'Windows':
	playsound = _playsound_crappy_win
del system

#test
playsound('/home/vlad/Desktop/sound/file_test_name.wav')
