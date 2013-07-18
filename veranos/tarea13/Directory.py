import os

path = os.getcwd()

def createDirectory():
	folder = 'GIF_IMAGES'
	folder2 = 'PIX_IMAGES'
	
	if not os.path.isdir(folder):
	    os.mkdir(folder)

	if not os.path.isdir(folder2):
	    os.mkdir(folder2)

	os.chdir(path) # back to directory
	return(folder, folder2)


def movedir(destination, origin=os.getcwd()):
	directory = os.path.join(origin, destination)
	os.chdir(directory)


def backDirectory():
	os.chdir(path) # back to directory


def creatGif():
	os.system('convert -delay 200 -quality 20 -size 200 -loop 0 *.png GIF.gif')
