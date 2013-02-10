import Image
from sys import argv
import time
from pylab import *
import math

PREWITT_X = [-1, 0, 1, -1, 0, 1, -1, 0, 1] 
PREWITT_Y = [1, 1, 1, 0, 0, 0, -1, -1, -1]

SOBEL_X = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
SOBEL_Y = [1, 2, 1, 0, 0, 0, -1, -2, -1]

debug = False

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

def calcularVecinosCruz(pixeles, indice, ancho):
	# primero el izquiero
	centro = (len(PREWITT_X) + 1) / 2 # mascara de 3x3
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

	return (vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)

def calcularVecinosDiagonales(pixeles, indice, ancho):
	# primero el izquiero arriba
	try:
		vecinoIzqArriba = max(pixeles[indice - (ancho + 1)])
	except:
		# si no tiene vecino izquierdo arriba
		vecinoIzqArriba = 0
	# ahora el derecho arriba
	try:
		vecinoDerArriba = max(pixeles[indice - (ancho - 1)])

	except:
		# si no tiene vecino derecho arriba
		vecinoDerArriba = 0
	# ahora el vecino izquieda abajo
	try:
		vecinoIzqAbajo = max(pixeles[indice + (ancho - 1)])
	except:
		# si no tiene vecinos izquierda abajo
		vecinoIzqAbajo = 0
	# el ultimo vecino... derecha abajo
	try:
		vecinoDerAbajo = max(pixeles[indice + (ancho + 1)])
	except:
		# si no tiene vecino derecha abajo
		vecinoDerAbajo = 0

	return (vecinoIzqArriba, vecinoDerArriba, vecinoIzqAbajo, vecinoDerAbajo)

def aplicarFiltro(pixeles, ancho):
	imagenFiltrada = list()

	for indice in range(len(pixeles)):
		#Sacamos los pixeles vecinos en cruz(arriba, abajo, der, izq)
		(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba) = \
											calcularVecinosCruz(pixeles, indice, ancho)
		
		# ya tenemos todos los vecinos validados, ahora creamos la nueva imagen
		nuevoPixel = max(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
		imagenFiltrada.append((nuevoPixel, nuevoPixel, nuevoPixel))

	return imagenFiltrada

def ordenarVecinos(vecinosTotales, pixelActual):
	vecinosTotales = list(vecinosTotales)
	vecinosOrdenados = list()

	vecinosOrdenados.append(vecinosTotales.pop(4)) # izq arriba
	vecinosOrdenados.append(vecinosTotales.pop(3)) # arriba
	vecinosOrdenados.append(vecinosTotales.pop(3)) # der arriba
	vecinosOrdenados.append(vecinosTotales.pop(0)) # izq
	vecinosOrdenados.append(max(pixelActual) )          # actual
	vecinosOrdenados.append(vecinosTotales.pop(0)) # der
	vecinosOrdenados.append(vecinosTotales.pop(1)) # izq abajo
	vecinosOrdenados.append(vecinosTotales.pop(0)) # abajo
	vecinosOrdenados.append(vecinosTotales.pop(0)) # der abajo

	return vecinosOrdenados


def aplicarConvolucion(pixeles, ancho):
	imagenConvolucion = list()
	imagenNormalizada = list()

	MINN = 1000
	MAXN = 1

	for indice in range(len(pixeles)):
		# sacamos los vecinos en cruz
		#(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
		vecinosCruz = 	calcularVecinosCruz(pixeles, indice, ancho)
		
		# sacamos los vecinos en diagonal
		#(vecinoIzqArriba, vecinoDerArriba, vecinoIzqAbajo, vecinoDerAbajo) 
		vecinosDiagonales = calcularVecinosDiagonales(pixeles, indice, ancho)

		# sumamos todos los vecinos
		vecinosTotales = vecinosCruz + vecinosDiagonales
		# y ordenamos para multiplicar por la mascara centralizada
		vecinosOrdenados = ordenarVecinos(vecinosTotales, pixeles[indice])

		sumaX = 0
		sumaY = 0

		# multiplicaciones
		for i in range(len(vecinosOrdenados)):
			
			multiplicacionX = vecinosOrdenados[i] * PREWITT_X[i]
			multiplicacionY = vecinosOrdenados[i] * PREWITT_Y[i]

			sumaX = multiplicacionX + sumaX
			sumaY = multiplicacionY + sumaY

			#nuevoPixel = int(math.sqrt((sumaX ** 2) + (sumaY ** 2)))
			nuevoPixel = sumaX + sumaY


			if debug: print "++++", nuevoPixel

			# Validacion para convolucion
			if nuevoPixel > 255:
				nuevoPixel = 255

			if nuevoPixel < 0:
				nuevoPixel = 0

			# NORMALIZACION
			#Normalizar la imagen
			#d -> a[0,255]
			#chocar[min,max] actual
			#r = max -min;
			#Esto ya no lo entendi 
			#prop = 256/r;	
			#p= int(flour((p-min)*prop));
			if nuevoPixel < MINN:
				MINN = nuevoPixel
			if nuevoPixel > MAXN:
				MAXN = nuevoPixel
			valorNuevo = (nuevoPixel - MINN) / (MAXN- MINN) * 255
			# FIN DE NORMALIZACION
			

		imagenNormalizada.append((valorNuevo, valorNuevo, valorNuevo))
		imagenConvolucion.append((nuevoPixel, nuevoPixel, nuevoPixel))
	return (imagenConvolucion, imagenNormalizada)




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

	tiempoConvolucionInicio = time.time()	
	(convolucion, normalizada) = aplicarConvolucion(grises, ancho)
	guardarImagen(convolucion, ancho, alto, "salidaCONVO.png")
	guardarImagen(normalizada, ancho, alto, "salidaNORMA.png")
	tiempoConvolucionFinal = time.time()

	print "Tiempos"
	print "En escala a grises: ", tiempoGrisesFinal - tiempoGrisesInicio, "segundos"
	print "En umbral: ", tiempoUmbralFinal - tiempoUmbralInicio, "segundos"
	print "En filtro: ", tiempoFiltroFinal - tiempoFiltroInicio, "segundos"
	print "En convolucion y normalizacion: ", tiempoConvolucionFinal - tiempoConvolucionInicio, "segundos"
	return


############# CONFIGURACION DEL PROGRAMA ##############
## PARAMETROS DE ENTRADA                              #
#argv[1] = (string)nombre de la imagen a procesar     #
#argv[2] = (int)Rango minimo - para el umbral         #
#argv[3] = (int)Rango maximo - para el umbral         #
#######################################################
main(argv[1])
