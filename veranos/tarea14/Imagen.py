import Image

class Imagen(object):
	def __init__(self, im, id):
		self.pixeles = im.load()
		self.w = im.size[0]
		self.h = im.size[1]
		self.bordes = list()
		self.id = id