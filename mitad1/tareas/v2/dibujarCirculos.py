'''
import Image, ImageDraw

im = Image.open("sol.png")

draw = ImageDraw.Draw(im)
draw.ellipse((60, 60, 40, 40), fill=128)
del draw 

im.save('output.png')
im.show()
'''
from PIL import Image, ImageDraw

im = Image.open("sol.png")

x, y =  im.size
eX, eY = 30, 60 #Size of Bounding Box for ellipse

bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
draw = ImageDraw.Draw(im)
draw.ellipse((10, 10, 40, 40), fill=128)
del draw

im.save("output.png")
im.show()