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
		self.imagenOriginal = (self.imagen.copy()).load()
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
				gx = sum(sum(vecindad * sobX))
				gy = sum(sum(vecindad * sobY))

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
				# 0 = NEGRO || 1 = BLANCO
				nuevoPixel = (0, 255)[min(pixeles[x,y]) > RANGO] # operador ternario
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)				
		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()
		print "Listo"	
		return 

	def buscarTumores(self, abrir, nombreImagenSalida="salidaOBJETOS.png"):
		print "Buscando objetos..."
		pixeles = self.imagen.load()
		draw = ImageDraw.Draw(self.imagen)
		negro = (0, 0, 0) # color del posible tumor
		centro = (1, 1, 1)
		objeto = 0
		ctumor = 0
		pixelesCola = list()
		pixelesVisitados = dict()

		for x in range(self.ancho): # cliclo principal
			for y in range(self.alto): # ciclo principal
				# buscamos el primer pixel negro para agregarlo como candidato
				if negro == pixeles[x,y]:
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
								# aseguramos que sea negro, que no este en la cola y								
								# que no se haya visitado mas aparte que no salga 
								# de las dimensiones de la imagen
								if mx >= 0 and my >= 0 and mx < self.ancho and my < self.alto\
									and pixeles[mx, my] == negro\
									 and (mx, my) not in pixelesCola\
									  and not pixelesVisitados.has_key((mx, my)):
									pixelesCola.append((mx, my)) #agreamos el vecino a la cola
									pixelesVisitados[mx, my] = True # agreamos visitados
						masa.append(pixelesCola.pop(0)) # borramos el candidato analizado
					
					#CENTRO DE MASA
					xmin = xmax = masa[0][0]
					ymin = ymax = masa[0][1]

					# puntos cardinales de la imagen
					for pixel in masa: 
						if pixel[0] < xmin:
							xmin = pixel[0]
						if pixel[0] > xmax:
							xmax = pixel[0]
						if pixel[1] < ymin:
							ymin = pixel[1]
						if pixel[1] > ymax:
							ymax = pixel[1]

					# pintamos siempre y cuando cumplan con las caracteristicas del tumor
					if len(masa) > 800 and len(masa) < 2000:
						# eliminamos masas demasiado pequenas y demasiado grandes
						nuevoColor = random.randrange(0,255)
						nuevoColor2 = random.randrange(0,255)
						nuevoColor3 = random.randrange(0,255)
						for pixel in masa: 
							pixeles[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)

						puntoCentro = (xmin+xmax)/2, (ymin+ymax)/2 # centro del objeto
						pixeles[puntoCentro] = centro

						base = xmax - xmin
						altura = ymax - ymin

						pixelesTotales = base * altura

						#rangoMin = pixelesTotales - 3500 # si
						#rangoMax = pixelesTotales + 1500 # si

						rangoMin = pixelesTotales - 3200 
						rangoMax = pixelesTotales + 800

						#print "objeto", objeto, "| masa total:", len(masa)
						#print "base: ", base, "altura:", altura
						#print "cuadro maagico de la masa:", pixelesTotales
						#print "rango:", rangoMin, "|", rangoMax

						print "tumor en:", puntoCentro
						
						# puede ser tumor
						tumor = False
						for i in range(rangoMin, rangoMax):
							if i == len(masa):
								tumor = True
								break
						
						if tumor:
							#print "Tumor"
							ctumor += 1
							draw.text(puntoCentro, "Tumor"+str(ctumor), fill="red") 
							#draw.line((10,10, 30,10), fill=128)
							#draw.line((10,10, 30,10), fill=128)
							#draw.line((10,10, 30,10), fill=128)
							#draw.line((10,10, 30,10), fill=128)
						else:
							objeto += 1
							draw.text(puntoCentro, "Masa"+str(objeto), fill="green")    					
						print "--------------------"
					else:
						pass 
				
		self.imagen.save(nombreImagenSalida)
		abrir = True
		if abrir:
			self.imagen.show()	
		print "listo"
		return 

	

	


