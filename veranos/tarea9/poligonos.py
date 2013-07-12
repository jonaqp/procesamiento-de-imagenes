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
		self.obIma = imagen
		self._objetos = list()

	def aplicarGris(self):
		print "Aplicando gris..."

		# creamos una copia para no modificar la imagen original
		nuevaImagen = Image.new('RGB', (self.obIma.ancho, self.obIma.alto))
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
		nuevaImagen = Image.new('RGB', (self.obIma.ancho, self.obIma.alto))
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
		# lista que contendra los pixeles tipo esquina
		pixelesEsquinas = list()

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
					pixelesEsquinas.append((x,y))

		imagenCopia.show()
		imagenCopia.save('SalidaEsquinas.png')
		print 'LISTO'  
		return pixelesEsquinas

	def buscarObjetos(self, imagenBase, elemento='negro'):
		print 'Buscando objetos...'

		imagenCopia = imagenBase.copy()
		tempPix = imagenCopia.load() 

		# 0 = negro || 255 = blanco
		if elemento == 'blanco': # elemento a buscar
			objeto = (255, 255, 255) 
		else: 
			objeto = (0, 0, 0) 

		print '    Buscando pixeles', elemento +'s'

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
					self._objetos.append(masa)

					
					nuevoColor = random.randrange(0,255)
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos
						tempPix[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)

		imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaObjetos.png') # guardamos el archivo
		print 'LISTO' 


	''' MEJORA: HACER QUE DIGA CUANTOS LADOS TIENE
		EL POLIGONO Y MUESTRE LOS LADOS QUE DETECTO. '''
	def dibujarLineas(self, pixelesDetectados, imagen):
		# METODO PENDIENTE
		draw = ImageDraw.Draw(imagen)

		for i in range(len(pixelesDetectados)-1):
			draw.line((pixelesDetectados[i][0], pixelesDetectados[0][1],\
						 pixelesDetectados[i+1][0], pixelesDetectados[i+1][0]), fill='red')

	

	def cajaEnvolvente(self, forma, imagen, mensaje=''):
		# Recibe un objeto y en el busca sus cordenadas minimas en eje x, eje y
		draw = ImageDraw.Draw(imagen) # creamos un objeto para dibujar

		minX = self.obIma.ancho
		maxX = 0
		minY = self.obIma.alto
		maxY = 0

		# recorremos el objeto que queremos encerrar
		for x,y in forma:	
			if x < minX:
				minX = x
			if x > maxX:
				maxX = x
			if y < minY:
				minY = y
			if y > maxY:
				maxY = y

		# descartamos aquellos objetos que sean muy chicos
		if minX < maxX and minY < maxY: 
			if not mensaje:
				# encerramos en un cuadrado el objeto recibido como parametro
				draw.rectangle(((minX, minY), (maxX, maxY)), outline="red")
			else:
				# escribimos en el punto centro del objeto el mensaje recibido como parametro
				puntoCentro = (minX+maxX)/2, (minY+maxY)/2 # centro del objeto
				draw.text(puntoCentro, mensaje, fill="green")

	
	def detectarPoligonos(self, imagenBase, pixelesEsquinas):
		poligonos = list() # guarda las poligonos detectados

		# creamos una copia para no modificar la imagen original
		imagenCopia = imagenBase.copy()
		pixelesCopia = imagenCopia.load() 

		# buscamos los objetos tipo borde de cada figura
		self.buscarObjetos(imagenBase) # le mandamos la imagen para que busque bordes
		
		# Algoritmo:
		# ahora que ya tenemos todos los bordes y los pixeles tipo esquina
		# el algoritmo trata de recorrer los bordes por figura y si el borde se topa con 
		# mas de 3 esquinas significa que es un poligono.

		# recorremos los objetos detectados
		for objeto in self._objetos:
			lado = 0
			for pixel in objeto:
				if pixel in pixelesEsquinas:
					lado += 1
					self.pintarVecinos(pixel[0], pixel[1], pixelesCopia)
			if lado >= 3: #significa que es un poligono de al menos 3 lados
				self.cajaEnvolvente(objeto, imagenCopia, 'poligono')
				poligonos.append(objeto)

		imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaPoligonos.png') # guardamos el archivo
		print 'Detectando poligonos...'
		print 'LISTO'
		return poligonos


def main(nombreImagen, rangoBinarizacion):
	im = Imagen(nombreImagen) # creamos el objeto imagen
	ad = AdministradorImagen(im) # le aplicamos las mejoras necesarias

	# aplicamos grises
	imaGris = ad.aplicarGris()

	# aplicar binarizacion
	imaBinarizada = ad.aplicarBinarizacion(imaGris, rangoBinarizacion)

	# detectar esquinas
	pixelesEsquinas = ad.detectarEsquinas(imaBinarizada)

	# detectar poligonos
	poligonos = ad.detectarPoligonos(imaBinarizada, pixelesEsquinas)

	





######## PARAMATROS DEL PROGRAMA #######
# [1] =(string) nombre de la imagen
# [2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(sys.argv[1], int(sys.argv[2]))



	 	


