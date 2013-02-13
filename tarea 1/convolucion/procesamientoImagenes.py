import Image
from sys import argv
import time
from pylab import *
import math


debug = False # controla todos los print del programa

def sobel(): 
	return([-1, 0, 1, -2, 0, 2, -1, 0, 1], \
		[1, 2, 1, 0, 0, 0, -1, -2, -1])

def prewiit():
	return([-1, 0, 1, -1, 0, 1, -1, 0, 1], \
	 	[1, 1, 1, 0, 0, 0, -1, -1, -1])

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
	try:
		MASCARA = argv[4]
		MASCARA = MASCARA.lower()
		MASCARA = globals()[MASCARA]
	except:
		MASCARA = raw_input("Mascara(SOBEL || PREWITT) : ")
		MASCARA = MASCARA.lower()
		MASCARA = globals()[MASCARA]
	try:
		RANGO_BINARIZACION = int(argv[5])
	except:
		RANGO_BINARIZACION = int(raw_input("Rango binarizacion: "))

	return(MIN, MAX, MASCARA, RANGO_BINARIZACION)

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
	#pixeles = (lista de listas) contiene todos los pixeles de la imagen
	# indice = (int) es la posicion del pixel actual
	# ancho = (int) es el ancho de la imagen 

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

	return (vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)

def calcularVecinosDiagonales(pixeles, indice, ancho):
	# pixeles = (lista de listas) contiene todos los pixeles de la imagen
	# indice = (int) es la posicion del pixel actual
	# ancho = (int) es el ancho de la imagen 

	# primero el izquiero arriba
	try:
		vecinoIzqArriba = max(pixeles[indice - (ancho + 1)])
	except:
		# si no tiene vecino izquierdo arriba
		vecinoIzqArriba = 0

	# ahora el derecha arriba
	try:
		vecinoDerArriba = max(pixeles[indice - (ancho - 1)])
	except:
		# si no tiene vecino derecha arriba
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
	vecinosOrdenados.append(max(pixelActual) )     # actual
	vecinosOrdenados.append(vecinosTotales.pop(0)) # der
	vecinosOrdenados.append(vecinosTotales.pop(1)) # izq abajo
	vecinosOrdenados.append(vecinosTotales.pop(0)) # abajo
	vecinosOrdenados.append(vecinosTotales.pop(0)) # der abajo

	return vecinosOrdenados

def normalizacion(pixelActual, MINN, MAXN):
	rango = MAXN - MINN
	prop = 256 / rango
	return int(math.floor((pixelActual - MINN) * prop))

def binarizacion(pixelActual, RANGO_BINARIZACION):
	if pixelActual > RANGO_BINARIZACION:
		return 255
	else:
		return 0

def aplicarConvolucion(pixeles, ancho, mascara, RANGO_BINARIZACION):
	imagenConvolucion = list()
	imagenNormalizada = list()
	imagenBinarizada = list()
	
	(mascaraX, mascaraY) = mascara()

	if debug: 
		print "X", mascaraX
		print "Y", mascaraY

	MINN = 1000 # numeros al azar
	MAXN = 1 # numeros al azar


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

		# multiplicaciones de matrices
		for i in range(len(vecinosOrdenados)):

			sumaX = (vecinosOrdenados[i] * mascaraX[i]) + sumaX
			sumaY = (vecinosOrdenados[i] * mascaraY[i]) + sumaY

			# Forma 1
			#nuevoPixel = int(math.sqrt((sumaX ** 2) + (sumaY ** 2)))
			# Forma 2
			nuevoPixel = sumaX + sumaY

			# Validacion para quitar pixeles innecesarios
			# NORMALIZACION
			pixelNormalizado = normalizacion(nuevoPixel, MINN, MAXN)

			if nuevoPixel > 255:
				nuevoPixel = 255
			if nuevoPixel < 0:
				nuevoPixel = 0			

			if nuevoPixel < MINN:
				MINN = nuevoPixel
			if nuevoPixel > MAXN:
				MAXN = nuevoPixel
			
			# BINARIZACION
			pixelBinarizado = binarizacion(nuevoPixel, RANGO_BINARIZACION)
			
		imagenConvolucion.append((nuevoPixel, nuevoPixel, nuevoPixel))
		imagenNormalizada.append((pixelNormalizado, pixelNormalizado, pixelNormalizado))
		imagenBinarizada.append((pixelBinarizado, pixelBinarizado, pixelBinarizado))


	return (imagenConvolucion, imagenNormalizada, imagenBinarizada)

def mostrarResumen(MIN, MAX, MASCARA , RANGO_BINARIZACION):
	print "------------------------------------------------------"
	print "PARAMETROS NUMERICOS DEL PROGRAMA"
	print "rango MIN para blanco-negro(umbral):", MIN
	print "rango MAX para blanco-negro(umbral):", MAX
	print "Rango para binarizacion:", RANGO_BINARIZACION
	print "------------------------------------------------------"
	return

def main(NombreImagen):

	(MIN, MAX, MASCARA , RANGO_BINARIZACION) = generarDatos(argv)
	mostrarResumen(MIN, MAX, MASCARA , RANGO_BINARIZACION)

	(pixeles, ancho, alto) = lecturaImagen(NombreImagen)
	
	tiempoGrisesInicio = time.time()
	grises = convertirGrises(pixeles) # convertimos a grices
	guardarImagen(grises, ancho, alto, "salidaGRIS.png") # guardamos
	tiempoGrisesFinal = time.time()

	tiempoUmbralInicio = time.time()
#	umbral = aplicarUmbral(pixeles, MIN, MAX) # aplicamos umbral
#	guardarImagen(umbral, ancho, alto, "salidaUMBRAL.png")
	tiempoUmbralFinal = time.time()

	tiempoFiltroInicio = time.time()
	filtro = aplicarFiltro(pixeles, ancho) # aplicamos FILTRO(que se vea borrosa)
	guardarImagen(filtro, ancho, alto, "salidaFILTRO.png") # guardamos
	tiempoFiltroFinal = time.time()

	tiempoConvolucionInicio = time.time()	
	(convolucion, normalizada, binarizada) = aplicarConvolucion(grises, ancho, \
																MASCARA, RANGO_BINARIZACION)
	guardarImagen(convolucion, ancho, alto, "salidaCONVO.png")
	guardarImagen(normalizada, ancho, alto, "salidaNORMA.png")
	guardarImagen(binarizada, ancho, alto, "salidaBINARI.png")
	tiempoConvolucionFinal = time.time()

	print "TIEMPOS"
	print "En escala a grises: ", tiempoGrisesFinal - tiempoGrisesInicio, "segundos"
	print "En umbral: ", tiempoUmbralFinal - tiempoUmbralInicio, "segundos"
	print "En filtro: ", tiempoFiltroFinal - tiempoFiltroInicio, "segundos"
	print "En convolucion, normalizacion y binarizacion: ", \
							tiempoConvolucionFinal - tiempoConvolucionInicio, "segundos"
	return


############# CONFIGURACION DEL PROGRAMA ##############
## PARAMETROS DE ENTRADA                              #
#argv[1] = (string)nombre de la imagen a procesar     #
#argv[2] = (int)Rango minimo - para el umbral         #
#argv[3] = (int)Rango maximo - para el umbral         #
#argv[4] = (string) mascara a usar (sobel || prewiit) #
#argv[5] = (int)Rango para binarizacion               #
#######################################################
main(argv[1])
