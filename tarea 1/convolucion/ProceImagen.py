import Image
from pylab import *

class ProceImagen:
	def __init__(self, nombreImagen):
		self.nombreImagen = nombreImagen

	def lectura(self):
		im = Image.open(self.nombreImagen) # creamos el objeto imagen 
		pixeles = list(im.getdata()) # lista de todos los pixeles
		ancho, alto = im.size # sacamos las medidas de la imagen
		return(pixeles, ancho, alto)

	def guardar(self, pixeles, ancho, alto):
		outImg = Image.new("RGB",(ancho, alto)) # creamos un nuevo objeto imagen
		outImg.putdata(pixeles) # le pasamos la nueva lista de pixeles
		outImg.save(self.nombreImagen) # guardamos el archivo
		imshow(outImg) # lo prepara para mostrarla en un cuadro
		show() # la abrimos
		return