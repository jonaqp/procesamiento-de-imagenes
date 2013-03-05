import Image
from pylab import *

class Imagen:
	def __init__(self, nombreImagen):
		self.nombreImagen = nombreImagen

	def setNombreImagen(self, nuevoNombre):
		self.nombreImagen = nuevoNombre

	def lectura(self):
		im = Image.open(self.nombreImagen) # creamos el objeto imaetiquetasgen 
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

	def guardarEtiquetas(self, pixeles, ancho, alto, etiquetas):
		outImg = Image.new("RGB",(ancho, alto)) # creamos un nuevo objeto imagen
		outImg.putdata(pixeles) # le pasamos la nueva lista de pixeles
		outImg.save(self.nombreImagen) # guardamos el archivo
		imshow(outImg) # lo prepara para mostrarla en un cuadro
		for indice, valor in enumerate(etiquetas):
			plt.text(valor/alto, valor/ancho, "uno", fontsize = 10, \
				horizontalalignment='center', verticalalignment='center') 
		show() # la abrimos
		return


