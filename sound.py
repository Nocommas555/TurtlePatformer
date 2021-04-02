from time import sleep

def _playsound_linux(file_source):
	import subprocess
	subprocess.Popen(["aplay", file_source])

def _playsound_win(file_source):
    import subprocess
    subprocess.Popen(["python", "sound_win_slave.py", file_source])

from platform import system
system = system()
print(system)
if system == 'Linux':
	playsound = _playsound_linux
elif system == 'Windows':
	playsound = _playsound_win
del system
