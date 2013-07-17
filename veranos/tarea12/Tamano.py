import sys
import Image
import numpy
import math


def calcularRelacion(ancho, alto, new_w, new_h):
	''' Relacion entre las dimensiones de la nueva imagen
	    contra la imagen actual. '''
	pixelesAncho = (1.0*new_w)/ancho
	pixelesAlto = (1.0*new_h)/alto 
	return pixelesAncho, pixelesAlto
	

class Tamano(object):	
	def __init__(self, imagen):
		self.obPic = imagen

	def redimensionar(self, new_w, new_h):
		print 'Redimensionando a ', new_w,'x',new_h, "..."

		w = self.obPic.w
		h = self.obPic.h
		pixOriginales = self.obPic.pixeles
		
		pixelesAncho, pixelesAlto=\
					calcularRelacion(w, h, new_w, new_h)
		
		nuevaImagen = Image.new("RGB", (new_w, new_h)) # creamos la nueva imagen
		newPixeles = nuevaImagen.load() # cargamos los pixeles de la nueva imagen

		new_w = int(w*pixelesAncho)
		new_h = int(h*pixelesAlto)
		
		# recorremos los pixeles de la nueva imagen y le asignamos el valor del pixel
		# actual(esto es con ayuda de la relacion de pixeles)
		for x in range(new_w):
			for y in range(new_h):
				# convertimos a enteros, porque acceder a un pixel no se puede con doubles.
				newPixeles[x,y] = pixOriginales[int(x/pixelesAncho), int(y/pixelesAlto)]
		
		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save("SalidaTamano.png") # guardamos el archivo
		print 'LISTO'
		return nuevaImagen