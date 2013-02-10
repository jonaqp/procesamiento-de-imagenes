import Image
from sys import argv
import time
qfrom pylab import *

def generarDatos(argv):
	try:
		MIN = int(argv[2])
		if MIN < 0 or MIN > 255:
			MIN = 110
	except:
		MIN = int(raw_input("Rango minimo: "))
		if MIN < 0 or MIN > 255:
			MIN = 110
	try: 
		MAX = int(argv[3])
		if MAX < 0 or MAX > 255:
			MAX = 190
	except:
		MAX = int(raw_input("Rango maximo: "))
		if MAX < 0 or MAX > 255:
			MAX = 190

	return(MIN, MAX)

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

def calcularVecinos(pixeles, indice):
	return (vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)

def aplicarFiltro(pixeles, ancho):
	imagenFiltrada = list()

	for indice in range(len(pixeles)):
		#Sacamos los pixeles vecinos
		# primero el izquiero
		try:
			vecinoIzq = max(pixeles[indice - 1])
		except:
			# si no tiene vecino izquierdo
			vecinoIzq = 0
		# ahora el derecho
		try:
			vecinoDer = max(pixeles[indice + 1])
		except:
			# si no tiene vecino derecho
			vecinoDer = 0
		# ahora el vecino de arriba
		try:
			vecinoArriba = max(pixeles[indice - ancho])
		except:
			# si no tiene vecinos de arriba
			vecinoArriba = 0
		# el ultimo vecino... el de abajo
		try:
			vecinoAbajo = max(pixeles[indice + ancho])
		except:
			# si no tiene vecino abajo
			vecinoAbajo = 0

		# ya tenemos todos los vecinos validados, ahora creamos la nueva imagen

		nuevoPixel = max(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
		imagenFiltrada.append((nuevoPixel, nuevoPixel, nuevoPixel))
	return imagenFiltrada

def aplicarUmbral(pixeles, MIN, MAX):
	imagenUmbral = list()
	for bite in pixeles: 
		nuevoByte = sum(bite) / 3 #calculamos el promedio del pixel
		
		# condiciones para hacer blanco-negro
		if MIN >= nuevoByte:
			nuevoByte = 0
		if MAX <= nuevoByte:
			nuevoByte = 255

		imagenUmbral.append((nuevoByte, nuevoByte, nuevoByte))  

	return imagenUmbral

def aplicarConvolucion(filtrada):
	return 




def main(NombreImagen):

	(MIN, MAX) = generarDatos(argv)

	(pixeles, ancho, alto) = lecturaImagen(NombreImagen)
	
	tiempoGrisesInicio = time.time()
	grises = convertirGrises(pixeles) # convertimos a grices
	guardarImagen(grises, ancho, alto, "salidaGRIS.png") # guardamos
	tiempoGrisesFinal = time.time()

	tiempoUmbralInicio = time.time()
	umbral = aplicarUmbral(pixeles, MIN, MAX) # aplicamos umbral
	guardarImagen(umbral, ancho, alto, "salidaUMBRAL.png")
	tiempoUmbralFinal = time.time()

	tiempoFiltroInicio = time.time()
	filtro = aplicarFiltro(pixeles, ancho) # aplicamos FILTRO(que se vea borrosa)
	guardarImagen(filtro, ancho, alto, "salidaFILTRO.png") # guardamos
	tiempoFiltroFinal = time.time()


	convolucion = aplicarConvolucion(grises)
	guardarImagen(convolucion, ancho, alto, "salidaCONVO.png")


	print "Tiempos"
	print "En escala a grises: ", tiempoGrisesFinal - tiempoGrisesInicio, "segundos"
	print "En umbral: ", tiempoUmbralFinal - tiempoUmbralInicio, "segundos"
	print "En filtro: ", tiempoFiltroFinal - tiempoFiltroInicio, "segundos"
	return


############# CONFIGURACION DEL PROGRAMA ##############
## PARAMETROS DE ENTRADA                              #
#argv[1] = (string)nombre de la imagen a procesar     #
#argv[2] = (int)Rango minimo - para el umbral         #
#argv[3] = (int)Rango maximo - para el umbral         #
#######################################################
main(argv[1])