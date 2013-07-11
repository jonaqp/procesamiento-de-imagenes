import Image
import ImageDraw
import sys
import math
import numpy
import random


def obtenerVecinos(x, y, ancho, alto, pixeles):
	''' 
		Recibe el pixel actual(x,y), las dimensiones de la imagen y
	    los pixeles de la imagen de la cual obtenemos los vecinos.
	    Regresa una matriz de 3*3 con los vecinos del pixel, en caso
	    de no tener un vecino el campo se llena(opr default) con cero.
	'''
	vecindad = numpy.zeros((3,3))
	for my in range(y-1, y+2):
		for mx in range(x-1, x+2):				
			if mx >= 0 and my >= 0 and mx < ancho and my < alto:
				''' el numero [1] es porque, como es una imagen de grises en realidad
				    no nos importa si es [1] o [0] o [2], los RGB tienen el mismo valor '''
				# asignamos el vecino a la matriz
				vecindad[mx-(x-1), my-(y-1)] = pixeles[mx, my][1] 
	return vecindad



class Imagen(object):
	def __init__(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		self.pixeles = self.imagen.load()
		self.ancho = self.imagen.size[0]
		self.alto = self.imagen.size[1]
		print self.imagen.format, self.imagen.size, self.imagen.mode




class AdministradorImagen(object):
	def __init__(self, imagen):
		self._bordes = list()
		self.obIma = imagen

	def aplicarGris(self):
		print "Aplicando gris..."

		nuevaImagen = Image.new("RGB", (self.obIma.ancho, self.obIma.alto))
		newPixeles = nuevaImagen.load()

		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				p = self.obIma.pixeles[x,y]
				prom = sum(p)/3
				newPixeles[x,y] = (prom, prom, prom)

		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save('SalidaGRIS.png') # guardamos el archivo
		print 'LISTO' 
		return nuevaImagen

	def aplicarBinarizacion(self, imagenBase, RANGO):
		print 'Aplicando binarizacion...'

		pixelesBase = imagenBase.load()

		# creamos una copia para no modificar la imagen original
		nuevaImagen = Image.new("RGB", (self.obIma.ancho, self.obIma.alto))
		newPixeles = nuevaImagen.load() 

		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				# 0 = NEGRO || 255 = BLANCO
				nuevoPixel = (0, 255)[min(pixelesBase[x,y]) > RANGO] # operador ternario
				newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)				
		
		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save('SalidaBinarizacion.png') # guardamos el archivo
		print 'LISTO' 
		return nuevaImagen

	def pintarVecinos(self, x, y, pixelesCopia):
		for mx in range(x-1,x+2):
			for my in range(y-1,y+2):
				if mx>=0 and my>=0 and mx<self.obIma.ancho and my<self.obIma.alto:
					pixelesCopia[mx,my] = (255, 0, 0)


	def detectarEsquinas(self, imagenBase):
		print 'Detectando esquinas...'
		pixGris = imagenBase.load()

		# creamos una copia para no modificar la imagen original
		imagenCopia = imagenBase.copy()
		pixelesCopia = imagenCopia.load() 		


		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				vecindad = list()
				for mx in range(x-1,x+2):
					for my in range(y-1,y+2):
						if mx>=0 and my>=0 and mx<self.obIma.ancho and my<self.obIma.alto:
							vecindad.append(pixGris[mx, my][0])

				vecindad.sort()
				z = vecindad[len(vecindad)/2]

				if(z - pixGris[x,y][1]) != 0:
					self.pintarVecinos(x, y, pixelesCopia)

		imagenCopia.show()
		imagenCopia.save('SalidaEsquinas.png')
		print 'LISTO'   




def main(nombreImagen, rangoBinarizacion):
	im = Imagen(nombreImagen) # creamos el objeto imagen
	ad = AdministradorImagen(im) # le aplicamos las mejoras necesarias

	
	''' MEJORA :: Hacer que regresen la imagen y enviarla como parametro. 
		Se ahorraria.... 8 lineas por metodo
	'''

	# aplicamos grises
	imaGris = ad.aplicarGris()

	# aplicar binarizacion
	imaBinarizada = ad.aplicarBinarizacion(imaGris, rangoBinarizacion)

	# detectar esquinas
	ad.detectarEsquinas(imaBinarizada)

	





######## PARAMATROS DEL PROGRAMA #######
# [1] =(string) nombre de la imagen
# [2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(sys.argv[1], int(sys.argv[2]))



	 	


