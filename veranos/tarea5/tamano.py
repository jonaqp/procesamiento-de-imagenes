import sys
import Image
import numpy
import math


'''Funciona para agrandar pero la logica esta mal para achicar '''

def calcularRelacion(ancho, alto, newAncho, newAlto):
	''' Regla de tres simples. '''
	pixelesAncho = int(math.ceil(((newAncho*100) / ancho)/100.0))
	pixelesAlto = int(math.ceil(((newAlto*100) / ancho)/100.0))
	return pixelesAncho, pixelesAlto



class Imagen(object):
	def __init__(self, nombreImagen):
		self.ima = Image.open(nombreImagen)
		self.pixeles = self.ima.load()
		self.ancho = self.ima.size[0]
		self.alto = self.ima.size[1]
		
	@property
	def newAncho(self):
		return self._newAncho

	@newAncho.setter
	def newAncho(self, valor):
		self._newAncho = valor

	@property
	def newAlto(self):
		return self._newAlto

	@newAlto.setter
	def newAlto(self, valor):
		self._newAlto = valor

	def redimensionar(self):
		print 'Redimensionando...'
		pixelesAncho, pixelesAlto =\
					calcularRelacion(self.ancho, self.alto,\
									 self._newAncho, self._newAlto)


		nuevaImagen = Image.new("RGB",\
								(self._newAncho, self._newAlto))
		pixelesNew = nuevaImagen.load()

		for y in range(self.alto):
			inicioY = (y*pixelesAlto) 
			finalY = (y*pixelesAlto) + pixelesAlto
			for x in range(self.ancho):
				inicioX = (x*pixelesAncho)
				finalX = (x*pixelesAncho) + pixelesAncho
				for ny in range(inicioY, finalY):
					for nx in range(inicioX, finalX):
						try:
							pixelesNew[nx, ny] = self.pixeles[x, y]
						except:
							break

		nuevaImagen.show()
		nuevaImagen.save("SALIDA.png")

		return nuevaImagen


def main(nombreImagen, newAncho, newAlto):
	# creamos un objeto tipo imagen
	ima = Imagen(nombreImagen)
	ima.newAncho = newAncho
	ima.newAlto = newAlto 

	nuevaImagen = ima.redimensionar()
	

##################################################
# [1] - nombre de la imagen 					
# [2] - int: el nuevo ancho que tendra la imagen
# [3] - int: el nuevo alto que tendra la imagen 
##################################################
main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))




