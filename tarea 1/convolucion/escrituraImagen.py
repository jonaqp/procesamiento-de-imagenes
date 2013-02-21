import Image

class Imagen:
	def __init__(self, pixeles, ancho, alto, nombreImagen):
		self.pixeles = pixeles
		self.ancho = ancho
		self.alto = alto
		self.nombreImagen = nombreImagen 

	def guardarImagen(self):
		outImg = Image.new("RGB",(self.ancho, self.alto)) # creamos un nuevo objeto imagen
		outImg.putdata(self.pixeles) # le pasamos la nueva lista de pixeles
		outImg.save(self.nombreImagen) # guardamos el archivo
		imshow(outImg) # lo prepara para mostrarla en un cuadro
		show() # la abrimos
		return