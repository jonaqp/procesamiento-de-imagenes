class Grises:
	def __init__(self, pixeles, ancho):
		print "GRISES"
		self.pixeles = pixeles
		self.ancho = ancho


	def convertir(self):
		imagenGris = list()
		# recorremos la lista de bites para modificarlos  
		for bite in self.pixeles:
			# agregamos a la "nueva" imagen
			imagenGris.append((max(bite), max(bite), max(bite)))  
		return imagenGris