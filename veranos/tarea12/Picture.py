import Image

class Picture(object):
	def __init__(self, nombreImagen):
		self.im = Image.open(nombreImagen)
		self.pixeles = self.im.load()
		self.w = self.im.size[0]
		self.h = self.im.size[1]
		self.imReducida = None
		print self.im.format, 
		print self.im.size,
		print self.im.mode

