class Grises:
	def __init__(self, pixeles):
		self.pixeles = pixeles

	def convertirGrises(self):
	imagenGris = list()
	# recorremos la lista de bites para modificarlos  
	for bite in self.pixeles:
		# agregamos a la "nueva" imagen
		imagenGris.append((max(bite), max(bite), max(bite)))  
	return imagenGris