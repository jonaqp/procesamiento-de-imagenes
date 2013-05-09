import Image, math, numpy

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


class Lineas:
	def __init__(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		self.ancho = self.imagen.size[0]
		self.alto = self.imagen.size[1]
		self.imagenOriginal = (self.imagen.copy()).load() # nuevoooo
		print self.imagen.format, self.imagen.size, self.imagen.mode

	def detectarLineas(self, abrir, nombreImagenSalida="salidaLINEAS.png"):
		print "Detectando lineas..."
		pixeles = self.imagen.load()
		
		frequency = dict()
		line_matrix = dict()
		sobX, sobY = sobel()

		for x in range(self.ancho):
			for y in range(self.alto):
				vecindad = obtenerVecinos(x, y, self.ancho, self.alto, self.imagenOriginal)
				 
				if (gx < -1*10.0 or gx > 10.0) or (gy < -1*10.0 or gy > 10.0): # porque 10 ? 
					angulo = 0.0
					if gx > 0.0 and gy == 0.0: # 0
						angulo = 0.0
					elif gx < 0.0 and gy == 0.0: # 180
						angulo = 180.0
					if gx == 0.0 and gy > 0.0: # 90
						angulo = 90.0
					elif gx == 0.0 and gy < 0.0: # 270
						angulo = 270-0 
					else:
						angulo = (int(math.degrees(math.atan(gy/gx)))/12)*12 # porque 12 ?

					ro = (int((x*math.cos(angulo))+(y*math.sin(angulo)))/30)*30 # porque 30 ?
					line_matrix[x, y] = (angulo, ro)

					if not (angulo, ro) in frequency:
						frequency[(angulo, ro)] = 1
					else:
						frequency[(angulo, ro)] += 1
				else:
					line_matrix[x, y] = None

		for i in frequency.keys():
			if frequency[i] < 5:
				frequency.pop(i)

		pixeles_verticales = 0
		pixeles_horizontales = 0
		pixeles_diagonales = 0
		for x in range(self.ancho):
			for y in range(self.alto):
				if line_matrix[x, y] in frequency:
					if line_matrix[x, y][0] == 0.0 or line_matrix[x, y][0] == 180.0:
						pixeles_horizontales += 1
						pixeles[x, y] = (255, 0, 0)
					elif line_matrix[x, y][0] == 90.0 or line_matrix[x, y][0] == 270.0:
						pixeles_verticales += 1
						pixeles[x, y] = (0, 0, 255)
					else:
						pixeles_diagonales += 1
						pixeles[x, y] = (0, 255, 0)

		print "Numero de pixeles horizontales:", pixeles_horizontales
		print "Numero de pixeles verticales:", pixeles_verticales
		print "Numero de pixeles diagonales:", pixeles_diagonales

		self.imagen.save(nombreImagenSalida)
		if abrir:
			self.imagen.show()
		print "listo"
		return 