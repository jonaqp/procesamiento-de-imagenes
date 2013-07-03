import Image, numpy, math, random, ImageDraw
from Mascaras import Mascaras

def obtenerVecinos(x, y, ancho, alto, imagenOriginal, funcion):
	if funcion != 'roberts':
		vecindad = numpy.zeros((3,3))
		for my in range(y-1, y+2):
			for mx in range(x-1, x+2):				
				if mx >= 0 and my >= 0 and mx < ancho and my < alto:
					vecindad[mx-(x-1), my-(y-1)] = imagenOriginal[mx, my][1]
	else:
		vecindad = numpy.zeros((2,2))
		for my in range(y-1, y+1):
			for mx in range(x-1, x+1):				
				if mx >= 0 and my >= 0 and mx < ancho and my < alto:
					vecindad[mx-(x-1), my-(y-1)] = imagenOriginal[mx, my][1]

	return vecindad

def identificarMascara(funcion):
	ma = Mascaras()
	if funcion == 'sobel':
		mx = ma.arr_sobelX
		my = ma.arr_sobelY
	elif funcion == 'roberts':
		mx = ma.arr_robertsX
		my = ma.arr_robertsY
	elif funcion == 'prewitt':
		mx = ma.arr_prewittX
		my = ma.arr_prewittY   
	return (mx, my)

class Procesamiento:
	def __init__(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)
		self.ancho = self.imagen.size[0]
		self.alto = self.imagen.size[1]
		self.imagenOriginal = self.imagen.load()
		print self.imagen.format, self.imagen.size, self.imagen.mode


	def setImagen(self, nombreImagen):
		self.imagen = Image.open(nombreImagen)


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


	def aplicarConvolucion(self, funcion):
		print 'Aplicando convolucion y normalizacion con', funcion, '...'
		(mx, my) = identificarMascara(funcion)
		
		imagenX = numpy.zeros((self.ancho, self.alto))
		imagenY = numpy.zeros((self.ancho, self.alto))		

		for x in range(self.ancho):
			for y in range(self.alto):
				vecindad = obtenerVecinos(x, y, self.ancho, self.alto, self.imagenOriginal, funcion)
				gx = sum(sum(vecindad * mx))
				gy = sum(sum(vecindad * my))
				
				imagenX[x, y] = gx
				imagenY[x, y] = gy
	
		return (imagenX, imagenY)
		

	def normalizar(self, abrir, funcion):
		''' PENDIENTE : Falta limpiar este metodo. '''
		pixeles = self.imagen.load()
		
		imagenX, imagenY = self.aplicarConvolucion(funcion) # cargamos las imagenes

		numeroMenorX = imagenX.min()
		numeroMayorX = imagenX.max()
		for y in range(self.alto):
			for x in range(self.ancho):
				nuevoPixel = int(255 * (imagenX[x,y]-numeroMenorX) / (numeroMayorX-numeroMenorX)) 
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)

		self.imagen.save('normalizacion'+funcion.upper()+'X.png')
		if abrir:
			self.imagen.show()

		# - -  - -- - - - - - - - - - - - - - - - - - - - - -- - - -  - -
		self.setImagen('salidaFILTRO.png')
		pixeles = self.imagen.load()

		numeroMenorY = imagenY.min()
		numeroMayorY = imagenY.max()
		for y in range(self.alto):
			for x in range(self.ancho):
				nuevoPixel = int(255 * (imagenY[x,y]-numeroMenorY) / (numeroMayorY-numeroMenorY)) 
				pixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)

		self.imagen.save('normalizacion'+funcion.upper()+'Y.png')
		if abrir:
			self.imagen.show()
		
		print "listo"









