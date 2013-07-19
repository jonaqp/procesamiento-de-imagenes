# This code was taken of...
# https://code.google.com/p/python-learning-tools/source/browse/trunk/images2gif.py

import PIL
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import numpy as np

import os

class Gif(object):

    def readGif(self, filename):
        """ readGif(filename, asNumpy=True)
        Read images from an animated GIF file.  Returns a list of numpy 
        arrays, or, if asNumpy is false, a list if PIL images.
        """
        
        # Load file using PIL
        pilIm = Image.open(filename)   
        pilIm.seek(0)
        
        # Read all images inside
        images = []
        try:
            while True:
                # Get image as numpy array
                tmp = pilIm.convert() # Make without palette
                a = np.asarray(tmp)
                if len(a.shape)==0:
                    raise MemoryError("Too little memory to convert PIL image to array")
                # Store, and next
                images.append(tmp)
                pilIm.seek(pilIm.tell()+1)
        except EOFError:
            pass
        
        # Done
        return images

    def createGif(self):
        os.system('convert -delay 10 -quality 20 -size 200 -loop 0 *.png salidaGIF.gif')