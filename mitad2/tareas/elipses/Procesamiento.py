import Image, numpy, math, random, ImageDraw

def sobel():
	return ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], \
 			[[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

def obtenerVecinos(x, y, ancho, alto, imagenOriginal):
	vecindad = numpy.zeros((3,3))
	for my in range(y-1, y+2):
		for mx in range(x-1, x+2):				
			if mx >= 0 and my >= 0 and mx < ancho and my < alto:
				vecindad[mx-(x-1), my-(y-1)] = imagenOriginal[mx, my][1]
	return vecindad

class Procesamiento:
	def __init__(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		self.ancho = self.imagen.size[0]
		self.alto = self.imagen.size[1]
		self.imagenOriginal = self.imagen.load()
		print self.imagen.format, self.imagen.size, self.imagen.mode

	def setImagen(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		return

	def aplicarFiltro(self, abrir, nombreImagenSalida="salidaFILTRO.png"):
		print "Aplicando filtro..."
		pixeles = self.imagen.load()

		
		for x in range(self.ancho):
			for y in range(self.alto):
				vecindad = list() # reiniciamos
				for mx in range(x-1, x+2):
					for my in range(y-1, y+2):
						if mx >= 0 and my >= 0 and mx < self.ancho and my < self.alto:
							vecindad.append(self.imagenOriginal[x, y][0]) 
				vecindad.sort()
				nuevoPixel =  vecindad[len(vecindad) / 2]
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)
		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()
		print "listo"
		return

	def aplicarConvolucion(self, abrir, nombreImagenSalida="salidaCONVOLUCION.png"):
		print "Aplicando convolucion..."
		sobX, sobY = sobel()
		pixeles = self.imagen.load()
		
		for x in range(self.ancho):
			for y in range(self.alto):
				vecindad = obtenerVecinos(x, y, self.ancho, self.alto, self.imagenOriginal)
				gx = sum(sum(vecindad * sobX)) # gradiente x del pixel actual
				gy = sum(sum(vecindad * sobY)) # gradiente y del pixel actual

				xm = (gx ** 2) 
				ym = (gy ** 2)
				nuevoPixel = int(math.sqrt(xm + ym)) # pitagoras
				
				if nuevoPixel > 255:
					nuevoPixel = 255
				if nuevoPixel < 0:
					nuevoPixel = 0

				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)
		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()		
		print "listo"
		return

	def aplicarNormalizacion(self, abrir, nombreImagenSalida="salidaNORMALIZACION.png"):
		print "Aplicando normaliazacion..."
		pixeles = self.imagen.load()

		valores = self.imagen.getextrema() # El minimo y maximo de la imagen
		MIN = valores[0]
		MAX = valores[0][1]
		for i in valores:
			if i[0] < MIN:
				MIN = i[0]
			if i[1] > MAX:
				MAX = i[1]

		rango = MAX - MIN
		prop = 255.0 / rango

		for y in range(self.alto):
			for x in range(self.ancho):
				nuevoPixel = int(math.floor(pixeles[x, y][1] - MIN) * prop)
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)

		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()
		print "listo"
		return	

	def aplicarBinarizacion(self, abrir, RANGO, nombreImagenSalida="salidaBINARIZADA.png"):
		print "Aplicando binarizacion..."
		pixeles = self.imagen.load()

		for x in range(self.ancho):
			for y in range(self.alto):
				# 0 = NEGRO || 255 = BLANCO
				nuevoPixel = (0, 255)[min(pixeles[x,y]) > RANGO] # operador ternario
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)				

		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()
		print "Listo"	
		return 

	def buscarObjetosTipoBorde(self, abrir, rangoT=200, nombreImagenSalida="salidaOBJETOS.png"):
		print "Buscando objetos..."
		pixeles = self.imagen.load()
		# draw = ImageDraw.Draw(self.imagen)
		blanco = (255, 255, 255)
		objeto = 0
		pixelesCola = list()
		figuras = list()
		pixelesVisitados = dict()

		for x in range(self.ancho): # cliclo principal
			for y in range(self.alto): # ciclo principal
				# buscamos el primer pixel blanco(borde) para agregarlo como candidato
				# descartamos los bordes de la imagen
				if blanco == pixeles[x,y] and x >= 1 and y >= 1:
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
								# aseguramos que sea blanco(borde), que no este en la cola y
								# que no se haya visitado mas aparte que no salga 
								# de las dimensiones de la imagen
								if mx >= 0 and my >= 0 and mx < self.ancho and my < self.alto\
									and pixeles[mx, my] == blanco\
									 and (mx, my) not in pixelesCola\
									  and not pixelesVisitados.has_key((mx, my)):
									pixelesCola.append((mx, my)) #agreamos el vecino a la cola
									pixelesVisitados[mx, my] = True # agreamos visitados
						masa.append(pixelesCola.pop(0)) # borramos el candidato analizado

					nuevoColor = random.randrange(0,255)
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos						
						pixeles[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)
					figuras.append(masa)
					
		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()	

		print "listo"
		return figuras

	def dibujarTangente(self, abrir, figurasBordes, nombreImagenSalida="salidaTANGENTE.png"):
		print "Detectando tangentes..."
		pixeles = self.imagen.load()
		#draw = ImageDraw.Draw(self.imagen)
		
		contador = 0
		puntosInterseccionMedio = list()

		sobX, sobY = sobel()

		for elemento in figurasBordes:
			while contador < len(elemento):
				diferenteDeCero1 = False
				diferenteDeCero2 = False
				separados = False
				while not separados:
					while not(diferenteDeCero1 and diferenteDeCero2):
						# iteramos hasta encontrar 2 puntos que NO sean lineas rectas
						while not diferenteDeCero1:
							pixelRandom1 = random.choice(elemento)
							vecindadPixelRandom1 = obtenerVecinos(pixelRandom1[0], pixelRandom1[1], self.ancho, self.alto, self.imagenOriginal)
							gradienteXPixelRandom1 = sum(sum(vecindadPixelRandom1 * sobX)) # gradiente x del pixelRandom1
							gradienteYPixelRandom1 = sum(sum(vecindadPixelRandom1 * sobY)) # gradiente x del pixelRandom1
							if gradienteXPixelRandom1 != 0.0 and gradienteYPixelRandom1 != 0.0:
								print "A",
								diferenteDeCero1 = True
							else:
								elemento.remove(pixelRandom1)

						while not diferenteDeCero2:
							pixelRandom2 = random.choice(elemento)
							vecindadPixelRandom2 = obtenerVecinos(pixelRandom2[0], pixelRandom2[1], self.ancho, self.alto, self.imagenOriginal)
							gradienteXPixelRandom2 = sum(sum(vecindadPixelRandom2 * sobX)) # gradiente x del pixelRandom2
							gradienteYPixelRandom2 = sum(sum(vecindadPixelRandom2 * sobY)) # gradiente x del pixelRandom2
							if gradienteXPixelRandom2 != 0.0 and gradienteYPixelRandom2 != 0.0:
								print "B",
								diferenteDeCero2 = True
							else:
								elemento.remove(pixelRandom2)
						if 700>abs(pixelRandom1[0]-pixelRandom2[0]) and 700>abs(pixelRandom1[1]-pixelRandom2[1]):
							print "C"
							separados = True
						else:
							print ".",
							diferenteDeCero2 = False

				pixeles[pixelRandom1] = (255, 0, 0) # pintamos en la imagen el pixel seleccionado
				pixeles[pixelRandom2] = (255, 0, 0) # pintamos en la imagen el pixel seleccionado
				#draw.text(pixelRandom1, "PR1", fill="red") 
				#draw.text(pixelRandom2, "PR2", fill="red") 

				# calculamos las pendientes de los dos pixeles random
				pendientePixelRandom1 = gradienteXPixelRandom1 / gradienteYPixelRandom1 
				pendientePixelRandom2 = gradienteXPixelRandom2 / gradienteYPixelRandom2

				# si las pendientes son iguales, los pixeles son descartados
				lineaTangente1 = list()
				lineaTangente2 = list()

				if pendientePixelRandom1 != pendientePixelRandom2:
					# buscamos la linea tangente para el punto 1 escogido al azar
					for puntoX1Recta in range(-130, 130):
						puntoY1Recta = (pendientePixelRandom1 * ((pixelRandom1[0] + puntoX1Recta) - pixelRandom1[0])) + pixelRandom1[1]
						# para que no salga de las dimensiones de la imagen
						if (pixelRandom1[0] + puntoX1Recta) >= 0 and puntoY1Recta >= 0 and\
							(pixelRandom1[0] + puntoX1Recta) < self.ancho and puntoY1Recta < self.alto:
								pixeles[((pixelRandom1[0] + puntoX1Recta), puntoY1Recta)] = (0,0,255)
								lineaTangente1.append((pixelRandom1[0] + puntoX1Recta, puntoY1Recta))
					# buscamos la linea tangente para el punto 2 escogido al azar
					for puntoX2Recta in range(-130, 130):
						puntoY2Recta = (pendientePixelRandom2 * ((pixelRandom2[0] + puntoX2Recta) - pixelRandom2[0])) + pixelRandom2[1]
						# para que no salga de las dimensiones de la imagen
						if (pixelRandom2[0] + puntoX2Recta) >= 0 and puntoY2Recta >= 0 and\
							(pixelRandom2[0] + puntoX2Recta) < self.ancho and puntoY2Recta < self.alto:
								pixeles[((pixelRandom2[0] + puntoX2Recta), puntoY2Recta)] = (0,0,255)
								lineaTangente2.append((pixelRandom2[0] + puntoX2Recta, puntoY2Recta))

					puntoMedio = (((pixelRandom1[0] + pixelRandom2[0]) / 2), ((pixelRandom1[1] + pixelRandom2[1]) / 2))
					#draw.text(puntoMedio, "PM", fill="red") 
					pixeles[puntoMedio] = (0, 255, 0)

					# buscamos el punto de interseccion
					for pixel in lineaTangente1:
						if pixel in lineaTangente2:
							print "PI"
							pixeles[pixel] = (255, 255, 255)
							#draw.text(pixel, "X", fill="red") 
							puntosInterseccionMedio.append([puntoMedio, pixel])
					contador += 1

		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()
		print "listo"
		return puntosInterseccionMedio


	def votacionPixeles(self, abrir, puntosInterseccionMedio, nombreImagenSalida="salidaCENTROELIPSE.png"):
		print "buscando centros de elipses..."
		pixeles = self.imagen.load()
		votados = dict()

		for figura in puntosInterseccionMedio:
			puntoX = figura[0][0]
			puntoY = figura[0][1]
			for i in range(-90, 90):
				# para no salga de las dimensines
				if i >= 0 and i < self.ancho and i < self.alto:
					linea = int(puntoX) + i
					#pixeles[linea, puntoY] = (255,0,0) 
					if linea in votados:
						votados[(linea, puntoY)] += 1
					else:
						votados[(linea, puntoY)] = 1
		nuevo = votados.items()
		sorted(nuevo, key=lambda o: o[1])
		print nuevo[-1]
		pixeles[nuevo[-1][0]] = (255, 255 ,0)
		


		abrir = True
		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()
		print "listo"
		return











