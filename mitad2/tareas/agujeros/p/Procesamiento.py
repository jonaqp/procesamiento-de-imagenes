import Image, numpy, math, random, ImageDraw
import matplotlib.pyplot as plt



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

	def aplicarGris(self, abrir, nombreImagenSalida="salidaGRIS.png"):
		pixeles = self.imagen.load()
		print "Aplicando grises..."
		for x in range(self.ancho):
			for y in range(self.alto):
				(R, G, B) = pixeles[x, y]# obtenemos los bytes del pixel
				nuevoPixel = max(R, G, B) # el maximo
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)
		self.imagen.save(nombreImagenSalida)

		if abrir: # 
			self.imagen.show()
		print "listo"
		return

	def sumarFilas(self):
		print "sumando horizontales"
		pixeles = self.imagen.load()
		histograma_horizontal = numpy.zeros(self.ancho,float)		

		for x in range(self.ancho):
			for y in range(self.alto):
				histograma_horizontal[x] += pixeles[x,y][0]
		print "listo"
		return histograma_horizontal

	def sumarColumnas(self):
		print "sumando verticales"
		pixeles = self.imagen.load()
		histograma_vertical=numpy.zeros(self.alto,float)		

		for x in range(self.ancho):
			for y in range(self.alto):
				histograma_vertical[y] += pixeles[x,y][0]
		print "listo"
		return histograma_vertical

	def graficar(self,horizontal,vertical):
		plt.clf()
		fig=plt.subplot(111)
		topex=max(horizontal)
		topey=max(vertical)
		alto = self.alto
		ancho = self.ancho
		if ancho>alto:
			n=ancho
		else:
			n=alto
		if topex > topey:
			tope=topex
		else:
			tope=topey
		#print 'horixontal',horizontal
		#print 'vertical',vertical
		plt.ylim(-0.1 * tope,tope * 1.1)
		plt.xlim(-0.1*n,1.1*n)
		plt.title('Histograma')
		x=range(1,ancho+1)
		y=range(1,alto+1)
		plt.plot(x,horizontal,'r-',linewidth=2,label='horizontal')
		
		plt.plot(y,vertical,'b-',linewidth=2,label='vertical')
		
		box = fig.get_position()
		fig.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
		fig.legend(loc = 'upper center', bbox_to_anchor=(0.5, -0.05), fancybox = True, shadow = True, ncol = 1)
		
		#plt.show()
		return

	def minimosLocales(self,vector):
		minimos=list()
		media=sum(vector)/len(vector)
		media2=(max(vector)+min(vector))/2
		for i in range(1,len(vector)-1):
			if vector[i-1]>vector[i] and vector[i]<vector[i+1]:
				if vector[i]<media-40:
					minimos.append(i)
		return minimos

	def linasImaginarias(self, minimosX, minimosY):
		pixeles = self.imagen.load()
		lineasVerticales = list()
		lineasHorizontales = list()

		minimosX = minimosX[-10:]
		minimosY = minimosY[-10:] 

		for x in minimosX:
			for y in range(self.alto):
				#pixeles[x, y] = (255, 0, 0)
				lineasVerticales.append((x, y))

		for y in minimosY:
			for x in range(self.ancho):
				#pixeles[x, y] = (0, 0, 255)
				lineasHorizontales.append((x, y))						

		self.imagen.show()
		return lineasHorizontales, lineasVerticales

	def calcularCruces(self, lineasHorizontales, lineasVerticales):
		print "Buscando pixeles de posibles agujeros..."
		pixeles = self.imagen.load()
		draw = ImageDraw.Draw(self.imagen)
		frecuencia = dict()
		pixelesCruz = list()

		for i in lineasVerticales:
			if i in frecuencia:
				frecuencia[i] += 1
			else:
				frecuencia[i] = 1

		for j in lineasHorizontales:
			if j in frecuencia:
				frecuencia[j] += 1
				if frecuencia[j] > 1:
					pixelesCruz.append(j)
					pixeles[j] = (255,0,0)
			else:
				frecuencia[j] = 1

		self.imagen.show()
		print "listo"
		return pixelesCruz

	def aplicarUmbral(self, abrir, nombreImagenSalida="salidaUMBRAL.png"):
		pixeles = self.imagen.load()
		print "Aplicando umbral..."
		for x in range(self.ancho):
			for y in range(self.alto):
				(R, G, B) = pixeles[x, y]
				nuevoPixel = max(R, G, B)
				if nuevoPixel < 120: # comparamos contra el umbral
					nuevoPixel = 0
				else:
					nuevoPixel = 255
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)
		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()
		print "listo"
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
				# 0 = NEGRO || 255 = BLANCO
				nuevoPixel = (0, 255)[min(pixeles[x,y]) > RANGO] # operador ternario
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)				

		self.imagen.save(nombreImagenSalida)

		if abrir:
			self.imagen.show()
		print "Listo"	
		return 

	def buscarObjetos(self, abrir, pixelesCruz, rangoT=200, nombreImagenSalida="salidaOBJETOS.png"):
		print "Buscando objetos..."
		pixeles = self.imagen.load()
		draw = ImageDraw.Draw(self.imagen)
		blanco = (255, 255, 255)
		centro = (1, 1, 1)
		objeto = 0
		pixelesCola = list()
		pixelesVisitados = dict()

		for x in range(self.ancho): # cliclo principal
			for y in range(self.alto): # ciclo principal
				# buscamos el primer pixel blanco(borde) para agregarlo como candidato
				if blanco == pixeles[x,y]:
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

					# dos elementos al azar
					punto1 = random.choice(masa)
					punto2 = random.choice(masa)

					
					#CENTRO DE MASA 
					xmin = xmax = masa[0][0]
					ymin = ymax = masa[0][1]

					nuevoColor = random.randrange(0,255)
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos
						if pixel[0] < xmin:
							xmin = pixel[0]
						if pixel[0] > xmax:
							xmax = pixel[0]
						if pixel[1] < ymin:
							ymin = pixel[1]
						if pixel[1] > ymax:
							ymax = pixel[1]
						pixeles[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)


					puntoCentro = (xmin+xmax)/2, (ymin+ymax)/2 # centro del objeto
					
					objeto += 1
					#draw.text(puntoCentro, "PC"+str(objeto), fill="green") 
					if objeto != 1:
						pixeles[puntoCentro] = (255,255,1)
						draw.line((puntoCentro, punto1), fill=128)					
					
		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()	

		print "listo"
		return 
