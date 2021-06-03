from time import sleep
import subprocess

sounds = {}
next_id = 0


def sound_finished(id):
	return sounds[str(id)].poll() != None

def kill_all_sounds():
	for sound in sounds.values():
		sound.kill()

def _playsound_linux(file_source):
	global next_id

	sounds[str(next_id)] = subprocess.Popen(["aplay", file_source])
	next_id+=1
	return next_id-1

def _playsound_darwin(file_source):
	global next_id

	sounds[str(next_id)] = subprocess.Popen(["afplay", file_source])
	next_id+=1
	return next_id-1

def _playsound_win(file_source):
	global next_id

	sounds[str(next_id)] = subprocess.Popen(["python", "sound_win_slave.py", file_source])
	next_id+=1
	return next_id-1

from platform import system
system = system()
if system == 'Linux':
	playsound = _playsound_linux
elif system == 'Windows':
	playsound = _playsound_win
elif system == 'Darwin':
	playsound = _playsound_darwin
del system
