from sys import argv

class Datos:
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
