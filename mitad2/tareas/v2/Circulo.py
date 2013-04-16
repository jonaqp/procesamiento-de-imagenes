import Image, numpy, math, ImageDraw, random

def sobel():
	return ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], \
 			[[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

def obtenerVecinos(x, y, ancho, alto, pixeles):
	vecindad = numpy.zeros((3,3))
	for my in range(y-1, y+2):
		for mx in range(x-1, x+2):				
			if mx >= 0 and my >= 0 and mx < ancho and my < alto:
				vecindad[mx-(x-1), my-(y-1)] = pixeles[mx, my][1]
	return vecindad

def random_yellow():
    return (255, random.randint(100,255), random.randint(0, 50))

class Circulo:
	def __init__(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		self.ancho = self.imagen.size[0]
		self.alto = self.imagen.size[1]
		print self.imagen.format, self.imagen.size, self.imagen.mode

	def detectarCirculos(self, abrir, nombreSalida="salidaCIRCULO.png"):
		print "Buscando circulos de radio conocido..."
		pixeles = self.imagen.load()
		draw = ImageDraw.Draw(self.imagen)

		sobX, sobY = sobel()
		frequency = dict()
		circle_matrix = dict()

		for x in range(self.ancho):
			for y in range(self.alto):
				vecindad = obtenerVecinos(x, y, self.ancho, self.alto, pixeles)
				gx = sum(sum(vecindad * sobX))
				gy = sum(sum(vecindad * sobY))

				gradiente = math.sqrt(math.pow(gx, 2) + math.pow(gy, 2))
				if gradiente < -1*10.0 or gradiente > 10.0: # porque  10.0 ?
					cos_theta = (gx / gradiente)
					sen_theta = (gy / gradiente)
					theta = math.atan2(gy, gx)
					r = 60

					centro = (int(x-r*math.cos(theta+math.radians(90.0))),\
					 int(y-r*math.sin(theta+math.radians(90.0))))
					centro = ((centro[0]/10)*10, (centro[1]/10)*10) # porque 10 ?
					circle_matrix[x, y] = centro

					if not centro in frequency:
						frequency[centro] = 1
					else:
						frequency[centro] += 1
				else:
					circle_matrix[x, y] = None

		for i in frequency.keys():
			if frequency[i] < 10*8: # porque x*8? = es el procentaje de centros
				frequency.pop(i)
			
		counter = 1
		colors = dict()

		for i in frequency.keys():
			colors[i] = random_yellow()
			r = 2
			draw.ellipse((i[0]-r, i[1]-r, i[0]+r, i[1]+r), fill=(0,255,0))
			draw.text((i[0]+r+3, i[1]), ("C"+str(counter)), fill=(0,255,0))
			counter += 1

		for x in range(self.ancho):
			for y in range(self.alto):
				if circle_matrix[x, y] in frequency:
					try:
						pixeles[x, y] = colors[circle_matrix[x,y]]
					except:
						pass

		self.imagen.save(nombreSalida)
		if abrir:
			self.imagen.show()
		print "listo"
		return

	
