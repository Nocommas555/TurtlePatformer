import winsound, sys
winsound.PlaySound(sys.argv[1], winsound.SND_FILENAME | winsound.SND_NOSTOP)
