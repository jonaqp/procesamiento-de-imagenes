class Filtro:
	def __init__(self, pixeles, ancho):
		print "FILTRO"
		self.pixeles = pixeles
		self.ancho = ancho

	def aplicar(self):
		imagenFiltrada = list()
	 
		for indice in range(len(self.pixeles)):
			#Sacamos los pixeles vecinos
			# primero el izquiero
			try:
				vecinoIzq = max(self.pixeles[indice - 1])
			except:
				# si no tiene vecino izquierdo
				vecinoIzq = max(self.pixeles[indice])
			# ahora el derecho
			try:
				vecinoDer = max(self.pixeles[indice + 1])
			except:
				# si no tiene vecino derecho
				vecinoDer = max(self.pixeles[indice])
			# ahora el vecino de arriba
			try:
				vecinoArriba = max(self.pixeles[indice - self.ancho])
			except:
				# si no tiene vecinos de arriba
				vecinoArriba = max(self.pixeles[indice])
			# el ultimo vecino... el de abajo
			try:
				vecinoAbajo = max(self.pixeles[indice + self.ancho])
			except:
				# si no tiene vecino abajo
				vecinoAbajo = max(self.pixeles[indice])
	 
			# ya tenemos todos los vecinos validados, ahora creamos la nueva imagen
	 
			nuevoPixel = max(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
			imagenFiltrada.append((nuevoPixel, nuevoPixel, nuevoPixel))
		return imagenFiltrada