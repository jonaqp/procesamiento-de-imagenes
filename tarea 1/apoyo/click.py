from PIL import Image
from pylab import *
im = array(Image.open("pixel2.png"))
imshow(im)
print "please click 3 points"
x = ginput(3)
print "you clicked:",x
show()