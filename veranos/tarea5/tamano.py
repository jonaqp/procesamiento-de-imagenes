import sys
import Image
import numpy
import math


def calcularRelacion(ancho, alto, newAncho, newAlto):
	''' Relacion entre las dimensiones de la nueva imagen
	    contra la imagen actual. '''
	pixelesAncho = (1.0*newAncho)/ancho
	pixelesAlto = (1.0*newAlto)/alto 
	return pixelesAncho, pixelesAlto
	

class Imagen(object):
	def __init__(self, nombreImagen):
		self.ima = Image.open(nombreImagen)
		self.pixeles = self.ima.load()
		self.ancho = self.ima.size[0]
		self.alto = self.ima.size[1]
		print self.ima.format, self.ima.size, self.ima.mode
		
	###### Propiedades ##############
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
	###### Fin propiedades ############

	def redimensionar(self):
		print 'Redimensionando...'
		
		
		pixelesAncho, pixelesAlto=\
					calcularRelacion(self.ancho, self.alto, self._newAncho, self._newAlto)
		
		nuevaImagen = Image.new("RGB", (self._newAncho, self._newAlto)) # creamos la nueva imagen
		newPixeles = nuevaImagen.load() # cargamos los pixeles de la nueva imagen


		self._newAncho = int(self.ancho*pixelesAncho)
		self._newAlto = int(self.alto*pixelesAlto)
		
		# recorremos los pixeles de la nueva imagen y le asignamos el valor del pixel
		# actual(esto es con ayuda de la relacion de pixeles)
		for x in range(self._newAncho):
			for y in range(self._newAlto):
				# convertimos a enteros, porque acceder a un pixel no se puede con doubles.
				newPixeles[x,y] = self.pixeles[int(x/pixelesAncho), int(y/pixelesAlto)]

		
		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save("SALIDA.png") # guardamos el archivo


def main(nombreImagen, newAncho, newAlto):
	# creamos un objeto tipo imagen
	ima = Imagen(nombreImagen)
	ima._newAncho = newAncho
	ima._newAlto = newAlto 

	ima.redimensionar()
	

##################################################
# [1] - nombre de la imagen 					
# [2] - int: el nuevo ancho que tendra la imagen
# [3] - int: el nuevo alto que tendra la imagen 
##################################################
main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
