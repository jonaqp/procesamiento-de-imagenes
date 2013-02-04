import Image
import sys
from pylab import *

def lecturaImagen(NombreImagen):
	im = Image.open(NombreImagen) # creamos el objeto imagen 
	pixeles = list(im.getdata()) # lista de todos los pixeles
	ancho, alto = im.size # sacamos las medidas de la imagen
	return(pixeles, ancho, alto)

def guardarImagen(pixeles, ancho, alto, nombreImagen):
	outImg = Image.new("RGB",(ancho, alto)) # creamos un nuevo objeto imagen
	outImg.putdata(pixeles) # le pasamos la nueva lista de pixeles
	outImg.save(nombreImagen) # guardamos el archivo
	imshow(outImg) # lo prepara para mostrarla en un cuadro
	show() # la abrimos
	return

def convertirGrises(pixeles):
	imagenGris = list()
	# recorremos la lista de bites para modificarlos  
	for bite in pixeles:
		# agregamos a la "nueva" imagen
		imagenGris.append((max(bite), max(bite), max(bite)))  
	return imagenGris

def convertirFiltro(pixeles, ancho):
	imagenFiltrada = list()

	for indice in range(len(pixeles)):
		#Sacamos los pixeles vecinos
		# primero el izquiero
		try:
			vecinoIzq = max(pixeles[indice - 1])
		except:
			# si no tiene vecino izquierdo
			vecinoIzq = max(pixeles[indice])
		# ahora el derecho
		try:
			vecinoDer = max(pixeles[indice + 1])
		except:
			# si no tiene vecino derecho
			vecinoDer = max(pixeles[indice])
		# ahora el vecino de arriba
		try:
			vecinoArriba = max(pixeles[indice - ancho])
		except:
			# si no tiene vecinos de arriba
			vecinoArriba = max(pixeles[indice])
		# el ultimo vecino... el de abajo
		try:
			vecinoAbajo = max(pixeles[indice + ancho])
		except:
			# si no tiene vecino abajo
			vecinoAbajo = max(pixeles[indice])

		# ya tenemos todos los vecinos validados, ahora creamos la nueva imagen

		nuevoPixel = max(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
		imagenFiltrada.append((nuevoPixel, nuevoPixel, nuevoPixel))
	return imagenFiltrada

def main(NombreImagen):
	(pixeles, ancho, alto) = lecturaImagen(NombreImagen)
	
	grises = convertirGrises(pixeles) # convertimos a grices
	guardarImagen(grises, ancho, alto, "salidaGRIS.png") # guardamos

	filtro = convertirFiltro(pixeles, ancho) # aplicamos FILTRO(que se vea borrosa)
	guardarImagen(filtro, ancho, alto, "salidaFILTRO.png") # guardamos
	return

####################################################
# argv[1] => nombre de la imagen a precesar        #
####################################################
main(sys.argv[1])
