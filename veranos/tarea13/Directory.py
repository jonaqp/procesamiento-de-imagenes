import os

path = os.getcwd()

def createDirectory():
	folder = 'GIF_IMAGES'
	folder2 = 'PIX_IMAGES'
	
	if not os.path.isdir(folder):
	    os.mkdir(folder)
	else: # remove your content
		movedir(folder)
		os.system('rm *.png')
		backDirectory()

	if not os.path.isdir(folder2):
	    os.mkdir(folder2)
	else: # remove your content
		movedir(folder2)
		os.system('rm *.png')
		backDirectory()

	os.chdir(path) # back to directory
	return(folder, folder2)


def movedir(destination, origin=os.getcwd()):
	directory = os.path.join(origin, destination)
	os.chdir(directory)


def backDirectory():
	os.chdir(path) # back to directory


def creatGif():
<<<<<<< HEAD
	os.system('convert -delay 10 -quality 20 -size 200 -loop 0 *.png GIF.gif')
=======
	os.system('convert -delay 200 -quality 20 -size 200 -loop 0 *.png GIF.gif')
>>>>>>> 410b4aa672aed6ed76f37d85f198bf875baea0c2
