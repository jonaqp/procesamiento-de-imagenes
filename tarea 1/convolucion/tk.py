'''
from Tkinter import *
from ImageTk import PhotoImage
import Image

win = Tk()
im = Image.open("salidaGRIS.png")
imaObj = PhotoImage(im)
Label(win, image = imaObj).pack()
win.mainloop()
'''

from Tkinter import *
from ImageTk import PhotoImage
import Image

class App:
	def __init__(self, root):

		frame = Frame(root)
		frame.pack()
		#self.root = root

		self.button = Button(frame, text = "QUIT", fg = "red", command = frame.quit)
		self.button.pack(side = LEFT)

		self.btnOriginal = Button(frame, text = "Original", fg = "blue", command = self.original)
		self.btnOriginal.pack(side = LEFT)	

		im = Image.open("salidaGRIS.png")
		imaObj = PhotoImage(im)
		Label(root, image = imaObj).pack()		
	
	def original(self):
		im = Image.open("pixel2.png")
		imaObj = PhotoImage(im)
		#Label(self.root, image = imaObj).pack(side = BOTTOM)
		label.destroy()
		self.f5(im)

	def f5(self, im):
		im = ImageTk.PhotoImage(im)
		global label
		label = Label(image = im)
		label.image = im
		label.pack()



root = Tk()
app = App(root)
root.mainloop()