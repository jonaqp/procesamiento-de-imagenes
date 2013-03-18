def binarizacion(pixelActual, RANGO_BINARIZACION):
	if pixelActual < RANGO_BINARIZACION:
		return 255
	else:
		return 0

class Diferenciacion:
	def __init__(self, grises, filtro):
		print "DIFERENCIACION"
		self.grises = grises
		self.filtro = filtro

	def aplicar(self):
		MINN = 1000 # numeros al azar
		MAXN = 1 # numeros al azar

		imagenDiferencia = list()
		for i in range(len(self.grises)):
			nuevoPixel = abs(max(self.grises[i]) - max(self.filtro[i]))
			
			# BINARIZACION
			pixelBinarizado = binarizacion(nuevoPixel, 30)
			imagenDiferencia.append((pixelBinarizado, pixelBinarizado, pixelBinarizado))

		return imagenDiferencia
