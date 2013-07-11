import Image
import ImageDraw
import sys
import math
import numpy
import random

def sobel():
	'''Mascara de convolucion: Sobel. '''
	return ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], \
 			[[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

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

def angulo(p, q, r):
    return (q[1]-p[1])*(r[0]-p[0]) - (q[0]-p[0])*(r[1]-p[1])





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

	########## Propiedades #############
	''' MEJORA : quitar estas propiedades y adaptar el codigo. '''

	@property
	def imagenConvolucion(self):
		return self._imagenConvolucion

	@imagenConvolucion.setter
	def imagenConvolucion(self, valor):
		self._imagenConvolucion = valor

	@property
	def imagenBinarizacion(self):
		return self._imagenBinarizacion

	@imagenBinarizacion.setter
	def imagenBinarizacion(self, valor):
		self._imagenBinarizacion = valor
	########## Fin propiedades #########

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


	def aplicarConvolucion(self):
		print 'Aplicando convolucion...'

		# creamos una copia para no modificar la imagen original
		nuevaImagen = Image.new("RGB", (self.obIma.ancho, self.obIma.alto))
		newPixeles = nuevaImagen.load() 

		sobX, sobY = sobel() # cargamos la mascara
		
		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				# obtenemos todos los vecinos de pixel actual
				vecindad = obtenerVecinos(x, y, self.obIma.ancho, self.obIma.alto, self.obIma.pixeles)
				gx = sum(sum(vecindad * sobX)) # multiplicamos matrices para obtener los gradientes en x
				gy = sum(sum(vecindad * sobY)) # multiplicamos matrices para obtener los gradientes en y

				xm = (gx ** 2) # pitagoras
				ym = (gy ** 2) # pitagoras
				nuevoPixel = int(math.sqrt(xm + ym)) # pitagoras
				
				if nuevoPixel > 255:
					nuevoPixel = 255
				if nuevoPixel < 0:
					nuevoPixel = 0

				newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)
		
		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save('SalidaConvolucion.png') # guardamos el archivo
		self._imagenConvolucion = nuevaImagen
		print 'LISTO' 
		

	def aplicarBinarizacion(self, RANGO):
		print 'Aplicando binarizacion...'

		# creamos una copia para no modificar la imagen original
		nuevaImagen = Image.new("RGB", (self.obIma.ancho, self.obIma.alto))
		newPixeles = nuevaImagen.load() 

		convPixeles = self._imagenConvolucion.load()

		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				# 0 = NEGRO || 255 = BLANCO
				nuevoPixel = (0, 255)[min(convPixeles[x,y]) > RANGO] # operador ternario
				newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)				
		
		nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save('SalidaBinarizacion.png') # guardamos el archivo
		self._imagenBinarizacion = nuevaImagen
		print 'LISTO' 
		
	def buscarObjetos(self):
		print "Buscando objetos..."

		temp = Image.open('SalidaBinarizacion.png')
		tempPix = temp.load()

		# 0 = objetos || 255 = bordes
		objeto = (255, 255, 255) # elemento a buscar
		pixelesCola = list()
		pixelesVisitados = dict()

		for x in range(self.obIma.ancho): # cliclo principal
			for y in range(self.obIma.alto): # ciclo principal
				# buscamos el primer pixel para agregarlo como candidato
				if objeto == tempPix[x,y]:
					pixelesCola.append((x,y)) # agregamos el candidato a la cola

					masa = list() # el objeto que se forma con el candidato
					while pixelesCola > 0: 
						try:
							pixelesActual = pixelesCola[0] # asignos el candidato a analizar
							pixelesVisitados[x, y] = True # agreamos a visitados
						except:
							break # ya no hay elementos
						# recorremos sus vecinos
						for mx in range(pixelesActual[0]-1, pixelesActual[0]+2):
							for my in range(pixelesActual[1]-1, pixelesActual[1]+2):			
								# aseguramos que sea igual al objeto a buscar, que no este 
								# en la cola y que no se haya visitado mas aparte que no salga 
								# de las dimensiones de la imagen
								if mx>=0 and my>=0 and mx<self.obIma.ancho and my<self.obIma.alto\
								   and tempPix[mx, my] == objeto\
								     and (mx, my) not in pixelesCola\
								      and not pixelesVisitados.has_key((mx, my)):
								    pixelesCola.append((mx, my)) #agreamos el vecino a la cola
								    pixelesVisitados[mx, my] = True # agreamos visitados
						masa.append(pixelesCola.pop(0)) # borramos el candidato analizado
					self._bordes.append(masa) # agregamos el objeto a la lista de objetos

					
					nuevoColor = random.randrange(0,255)
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos
						tempPix[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)

		temp.show() # mostramos en ventana
		temp.save('SalidaObjetos.png') # guardamos el archivo
		print 'LISTO' 

	def jarvis(self, objeto):
		capaArriba = list()
		capaAbajo = list()

		objeto.sort()

		for coordenada in objeto:
			while len(capaArriba) > 1 and\
			 angulo(capaArriba[-2], capaArriba[-1], coordenada) >= 0:
				capaArriba.pop()

			while len(capaAbajo) > 1 and\
			 angulo(capaAbajo[-2], capaAbajo[-1], coordenada) <= 0:
				capaAbajo.pop()

			capaArriba.append(coordenada)
			capaAbajo.append(coordenada)
		return capaAbajo, capaArriba

	def convexhull(self):
		print 'Aplicando convexhull'

		# cargamos la imagen base
		temp = Image.open('SalidaBinarizacion.png')
		tempPix = temp.load()

		# y hacemos una copia para que no se modifique
		imagenCopia = temp.copy()
		pixelesCopia = imagenCopia.load()

		draw = ImageDraw.Draw(imagenCopia) # creamos un objeto para dibujar

		# recorremos los objetos tipos bordes detectados anteriormente
		for objetos in self._bordes:
			# enviar las coordenadas de cada borde
			capaAbajo, capaArriba = self.jarvis(objetos)
			# unir los puntos...
			# hasta "len(capaX)-1" para no tomar el ultimo punto esto
			# para cachar el error al momento de hacer las lineas
			for x in range(len(capaAbajo)-1):				
				draw.line([capaAbajo[x][0], capaAbajo[x][1], capaAbajo[x+1][0], capaAbajo[x+1][1]], 
					fill="red")

			for y in range(len(capaArriba)-1):				
				draw.line([capaArriba[y][0], capaArriba[y][1], capaArriba[y+1][0], capaArriba[y+1][1]], 
					fill="red")
			
		imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaConvexhull.png')
		print 'LISTO'

	def cajaEnvolvente(self):
		# cargamos la imagen base
		temp = Image.open('SalidaBinarizacion.png')
	   	
	   	# y hacemos una copia para que no se modifique
		imagenCopia = temp.copy()
		draw = ImageDraw.Draw(imagenCopia) # creamos un objeto para dibujar

		# recorremos los objetos tipos bordes detectados anteriormente
		for objetos in self._bordes:
			minX = self.obIma.ancho
			maxX = 0
			minY = self.obIma.alto
			maxY = 0
			for x,y in objetos:
				if x < minX:
					minX = x
				if x > maxX:
					maxX = x
				if y < minY:
					minY = y
				if y > maxY:
					maxY = y
	
			# eliminamos aquellos objetos que sean muy chicos
			if minX < maxX and minY < maxY: 
				print minX, minY, maxX, maxY
				draw.rectangle(((minX, minY),(maxX, maxY)), outline="red")

		imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaCajaEnvolvente.png')
		print 'LISTO'  

	def detectarEsquinas(self):
		gris = Image.open('SalidaGRIS.png')
		pixGris = gris.load()

		# creamos una copia para no modificar la imagen original
		imagenCopia = gris.copy()
		pixelesCopia = imagenCopia.load() 		


		for x in range(self.obIma.ancho):
			for y in range(self.obIma.alto):
				vecindad = list()
				for mx in range(x-1,x+2):
					for my in range(y-1,y+2):
						if mx>=0 and my>=0 and mx<self.obIma.ancho and my<self.obIma.alto:
							vecindad.append(pixGris[mx, my][0])


				vecindad.sort()


				z = len(vecindad)/2
				z = vecindad[z]

				
				
				if (z - pixGris[x,y][1]) != 0:
					pixelesCopia[x,y] = (255, 255, 0)


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
	ad.aplicarGris()

	'''
	# para buscar objetos o bordes es necesario convolucion y binarizacion
	ad.aplicarConvolucion()
	ad.aplicarBinarizacion(rangoBinarizacion)

	# buscamos objetos
	ad.buscarObjetos()

	# encerramos en una caja los objetos detectados    
	ad.cajaEnvolvente()

	# aplicar convexhull
	ad.convexhull()
	'''

	# detectar esquinas
	ad.detectarEsquinas()

	





######## PARAMATROS DEL PROGRAMA #######
# [1] =(string) nombre de la imagen
# [2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(sys.argv[1], int(sys.argv[2]))



	 	


