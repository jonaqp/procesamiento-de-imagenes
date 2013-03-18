import Image
from sys import argv
import time
from pylab import *
import math
import random


debug = False # controla todos los print del programa

def sobel(): 
	return([-1, 0, 1, -2, 0, 2, -1, 0, 1], \
		[1, 2, 1, 0, 0, 0, -1, -2, -1])

def prewiit():
	return([-1, 0, 1, -1, 0, 1, -1, 0, 1], \
	 	[1, 1, 1, 0, 0, 0, -1, -1, -1])

def generarDatosSalPimienta(argv):
	try:
		INTENSIDAD = float(argv[3])
		if (INTENSIDAD < 0.0 or INTENSIDAD > 1.0):
			print '''El parametro #3 debe ser un numero entre(0 - 1), cada vez que no cumpla
			el rango se asiganara .8 por defaul '''
			INTENSIDAD = 0.8
	except:
		INTENSIDAD = float(raw_input("Intensidad(Numero entre 0 - 1): "))
		if (INTENSIDAD < 0.0 or INTENSIDAD > 1.0):
			print '''El parametro #3 debe ser un numero entre(0 - 1), cada vez que no cumpla
			el rango se asiganara .8 por defaul '''
			INTENSIDAD = 0.8
	try:
		POLARIZACION = float(argv[4])
		if (POLARIZACION < 0 or POLARIZACION > 1):
			print '''El parametro #4 debe ser un numero entre(0 - 1), cada vez que no cumpla
			el rango se asiganara .8 por defaul '''
			POLARIZACION = 0.8
	except:
		POLARIZACION = float(raw_input("Polarizacion(Numero entre 0 -1 ): "))
		if (POLARIZACION < 0 or POLARIZACION > 1):
			print '''El parametro #4 debe ser un numero entre(0 - 1), cada vez que no cumpla
			el rango se asiganara .8 por defaul '''
			POLARIZACION = 0.8
	return(INTENSIDAD, POLARIZACION)


def generarDatosConvolucion(argv):
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
	for bite in pixepixelesles:
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

def calcularVecinosCruz(pixeles, indice, ancho, anchoH):
	#pixeles = (lista de listas) contiene todos los pixeles de la imagen
	# indice = (int) es la posicion del pixel actual
	# ancho = (int) es el ancho de la imagen 
	# anchoModificado = (int) es una variable de control

	# primero el izquiero
	vecinoIzq = indice - 1
	if vecinoIzq < 0:
		# las listas puede tener numeros negatios que siginica que empiezan desde atras
		# para eso este if... en caso de ser negativo significa que no tiene vecino
		vecinoIzq = 0
	else:
		if vecinoIzq == ancho:
			# significa que esta tocando el pixel final de la linea de arriba
			vecinoIzq = 0
		else:
			vecinoIzq = list(pixeles[vecinoIzq]) #tiene vecino
			vecinoIzq.sort() #tiene vecino
			vecinoIzq = vecinoIzq[1] #tiene vecino		
		
	# vecino Arriba
	vecinoArriba = indice - anchoH 
	if vecinoArriba <= 0:
		# las listas puede tener numeros negatios que siginica que empiezan desde atras
		# para eso este if... en caso de ser negativo significa que no tiene vecino
		vecinoArriba = 0
	else:
		vecinoArriba = list(pixeles[vecinoArriba - 1])
		vecinoArriba.sort()
		vecinoArriba = vecinoArriba[1]

	# ahora el derecho
	try:
		if indice == ancho:
			vecinoDer = 0
		else:
			base = list(pixeles[indice + 1])
			base.sort()
			vecinoDer = base[1]
	except:
		# si no tiene vecino derecho
		vecinoDer = 0
	'''
	# ahora el vecino de arriba
	try:
		base = list(pixeles[indice - ancho])
		base.sort()
		vecinoArriba = base[1]
	except:
		# si no tiene vecinos de arriba
		vecinoArriba = 0
	'''

	# el ultimo vecino... el de abajo
	try:
		vecinoAbajo = list(pixeles[indice + anchoH +1])
		vecinoAbajo.sort()
		vecinoAbajo = vecinoAbajo[1]
	except:
		# si no tiene vecino abajo
		vecinoAbajo = 0
	return (vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)

def calcularVecinosDiagonales(pixeles, indice, ancho):
	# pixeles = (lista de listas) contiene todos los pixeles de la imagen
	# indice = (int) es la posicion del pixel actual
	# ancho = (int) es el ancho de la imagen 
	# anchoM = (int) es una variable de control

	# vecino izquiero arriba
	vecinoIzqArriba = indice - (ancho + 1)
	if vecinoIzqArriba < 0:
		# las listas puede tener numeros negatios que siginica que empiezan desde atras
		# para eso este if... en caso de ser negativo significa que no tiene vecino
		vecinoIzqArriba = 0
	else:
		vecinoIzqArriba = list(pixeles[vecinoIzqArriba])
		vecinoIzqArriba.sort()
		#base = list(pixeles[indice - (ancho + 1)])
		vecinoIzqArriba = vecinoIzqArriba[1]

	# ahora el derecha arriba
	vecinoDerArriba = indice - (ancho - 1)
	if vecinoDerArriba < 0:
		# las listas puede tener numeros negatios que siginica que empiezan desde atras
		# para eso este if... en caso de ser negativo significa que no tiene vecino
		vecinoDerArriba = 0
	else:
		vecinoDerArriba = list(pixeles[vecinoDerArriba])
		vecinoDerArriba.sort()
		#base = list(pixeles[indice - (ancho + 1)])
		vecinoDerArriba = vecinoDerArriba[1]

	''''
	# primero el izquiero arriba
	try:
		vecinoIzqArriba = list(pixeles[indice - (ancho + 1)])
		vecinoIzqArriba.sort()
		#base = list(pixeles[indice - (ancho + 1)])
		vecinoIzqArriba = vecinoIzqArriba[1]
	except:
		# si no tiene vecino izquierdo arriba
		vecinoIzqArriba = 0
	
	# ahora el derecha arriba
	try:
		base = list(pixeles[indice - (ancho - 1)])
		base.sort()
		vecinoDerArriba = base[1]
	except:
		# si no tiene vecino derecha arriba
		vecinoDerArriba = 0
	'''

	# ahora el vecino izquieda abajo
	try:
		base = list(pixeles[indice + (ancho - 1)])
		base.sort()
		vecinoIzqAbajo = base[1]
	except:
		# si no tiene vecinos izquierda abajo
		vecinoIzqAbajo = 0
	# el ultimo vecino... derecha abajo
	try:
		base =  list(pixeles[indice + (ancho + 1)])
		base.sort()
		vecinoDerAbajo = base[1]
	except:
		# si no tiene vecino derecha abajo
		vecinoDerAbajo = 0


	return (vecinoIzqArriba, vecinoDerArriba, vecinoIzqAbajo, vecinoDerAbajo)

def aplicarFiltro(pixeles, ancho):
	imagenFiltrada = list()
	anchoH = ancho

	for indice in range(len(pixeles)):
		#Sacamos los pixeles vecinos en cruz(arriba, abajo, der, izq)
		(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba) = \
											calcularVecinosCruz(pixeles, indice, ancho, anchoH)
		if anchoH == indice - 1:
			#incremento
			anchoH = anchoH + (ancho + 1)

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
	if pixelActual < RANGO_BINARIZACION:
		return 255
	else:
		return 0

def aplicarConvolucion(pixeles, ancho, mascara, RANGO_BINARIZACION):
	imagenConvolucion = list()
	imagenNormalizada = list()
	imagenBinarizada = list()
	nuevoA = ancho
	
	(mascaraX, mascaraY) = mascara()

	if debug: 
		print "X", mascaraX
		print "Y", mascaraY

	MINN = 1000 # numeros al azar
	MAXN = 1 # numeros al azar


	for indice in range(len(pixeles)):
		# sacamos los vecinos en cruz
		#(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)
		vecinosCruz = calcularVecinosCruz(pixeles, indice, ancho, nuevoA)
		#vecinosDiagonales = calcularVecinosDiagonales(pixeles, indice, ancho)
		if nuevoA == indice -1:
			#incremento
			nuevoA = nuevoA + (ancho + 1)

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
			nuevoPixel = int(math.sqrt((sumaX ** 2) + (sumaY ** 2)))
			# Forma 2
			#nuevoPixel = sumaX + sumaY

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

def aplicarDiferenciacion(grises, filtro):
	MINN = 1000 # numeros al azar
	MAXN = 1 # numeros al azar

	imagenDiferencia = list()
	for i in range(len(grises)):
		nuevoPixel = abs(max(grises[i]) - max(filtro[i]))
		'''
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
		'''
		
		# BINARIZACION
		pixelBinarizado = binarizacion(nuevoPixel, 30)

		imagenDiferencia.append((pixelBinarizado, pixelBinarizado, pixelBinarizado))

	return imagenDiferencia

def quitarSal(pixeles, imagenSalada, ancho):
	imagenDesabrida = list()

	nuevoA = ancho
	for indice in range(len(pixeles)):
		pixelActual = list(pixeles[indice])
		pixelActual.sort()
		pixelActual = (pixelActual[1]),
		vecinosCruz = calcularVecinosCruz(pixeles, indice, ancho, nuevoA)
		#vecinosDiagonales = calcularVecinosDiagonales(pixeles, indice, ancho)
		if nuevoA == indice -1:
			#incremento
			nuevoA = nuevoA + (ancho + 1)
		vecinos = pixelActual + vecinosCruz #+ vecinosDiagonales
		vecinos = list(vecinos)
		vecinos.sort()
		imagenDesabrida.append((vecinos[2], vecinos[2], vecinos[2]))
		
	return imagenDesabrida

def sal(pixeles, INTENSIDAD, POLARIZACION):
	imagenSalada = list()

	polarizacionBlanca = int(255 * POLARIZACION) 
	polarizacionNegra = int(255 - (255 * POLARIZACION))

	for indice in range(len(pixeles)):
		if random.random() <= INTENSIDAD:	
			if max(pixeles[indice]) < 100:
				# significa que encontro un pixel blanco
				imagenSalada.append((polarizacionBlanca, polarizacionBlanca, polarizacionBlanca))
			else:
				# significa que encontro un pixel negro
				imagenSalada.append((polarizacionNegra, polarizacionNegra, polarizacionNegra))
		else:
			# no se modifica el pixel
			imagenSalada.append(pixeles[indice])
	return imagenSalada

def main(NombreImagen):

	(pixeles, ancho, alto) = lecturaImagen(NombreImagen) # leemos la imagen

	try: # decide que hacer base a los  parametros de entrada
		salPimienta = False
		FN = argv[2]
		if "sal" == FN:
			salPimienta = True
	except:
		salPimienta = False
		
	# si se aplica salPimienta	
	if salPimienta:
		funcion = globals()[FN]
		(INTENSIDAD, POLARIZACION) = generarDatosSalPimienta(argv) # leemos los parametros

		tiempoSalInicio = time.time()
		imagenSalada = funcion(pixeles, INTENSIDAD, POLARIZACION)
		guardarImagen(imagenSalada, ancho, alto, "salidaSALADA.png") # guardamos
		tiempoSalFinal = time.time()

		tiempoSinSalInicio = time.time()
		imagenDesabrida = quitarSal(pixeles, imagenSalada, ancho)
		guardarImagen(imagenDesabrida, ancho, alto, "salidaDESABRIDA.png") # guardamos
		tiempoSinSalFinal = time.time()

		grises = convertirGrises(pixeles) # convertimos a grices
		#guardarImagen(grises, ancho, alto, "salidaGRIS.png") # guardamos

		filtro = aplicarFiltro(pixeles, ancho) # aplicamos FILTRO(que se vea borrosa)
		#guardarImagen(filtro, ancho, alto, "salidaFILTRO.png") # guardamos
		
		tiempoDiferenciacionInicio = time.time()
		diferenciacion = aplicarDiferenciacion(pixeles, filtro) # detectar bordes
		guardarImagen(diferenciacion, ancho, alto, "salidaDIFERENCIACION.png") 
		tiempoDiferenciacionFinal = time.time()


		print "TIEMPOS"
		print "Imagen de ", ancho,"x",alto, "pixeles" 
		print "En aplicar sal ", tiempoSalFinal - tiempoSalInicio,  "segundos"
		print "En quitar sal: ", tiempoSinSalFinal, tiempoSinSalInicio, "segundos"
		print "En diferenciacion: ", tiempoDiferenciacionFinal - \
											tiempoDiferenciacionInicio, "segundos"

	else:
		(MIN, MAX, MASCARA , RANGO_BINARIZACION) = generarDatosConvolucion(argv)
		mostrarResumen(MIN, MAX, MASCARA , RANGO_BINARIZACION)
		
		tiempoGrisesInicio = time.time()
		grises = convertirGrises(pixeles) # convertimos a grices
		guardarImagen(grises, ancho, alto, "salidaGRIS.png") # guardamos
		tiempoGrisesFinal = time.time()

		tiempoUmbralInicio = time.time()
	    #umbral = aplicarUmbral(pixeles, MIN, MAX) # aplicamos umbral
	    #guardarImagen(umbral, ancho, alto, "salidaUMBRAL.png")
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



############# CONFIGURACION DEL PROGRAMA ###################################################
## PARAMETROS DE ENTRADA                                                                   #
#argv[1] = (string)nombre de la imagen a procesar                                          #
#argv[2] = (int)Rango minimo - para el umbral  || (string) metodo a utilizar (salPimienta) #        
#argv[3] = (int)Rango maximo - para el umbral  || (double) intensidad                      #
#argv[4] = (string) mascara a usar (sobel || prewiit)  || (double) polarizacion            #
#argv[5] = (int)Rango para binarizacion                                                    #
############################################################################################
if debug:
	''' Comprobando la funcionabilidad 
	    del el metodo calcularVecinosCruz y calcularVecinosDiagonales 
	'''

	ancho = 2
	nuevoAncho = ancho
	print "DEBUG..."
	print "(vecinoIzq, vecinoDer, vecinoAbajo, vecinoArriba)"
	pixeles = [(2,3,4), (3,56,56), (45,45,23),
	           (67,34,111), (200,0,3), (23,89,10),
	           (65,12,75), (89,90,11), (65,87,9)]
	for indice in range(len(pixeles)):
		print nuevoAncho, "-", indice + 1, "-", 
		vecinos = calcularVecinosDiagonales(pixeles, indice, nuevoAncho, ancho)
		if nuevoAncho == indice -1:
			#incrementelo
			nuevoAncho = nuevoAncho + (ancho + 1)
		print vecinos
		print "-----------"

else:
	print "MAIN..."
	main(argv[1])	