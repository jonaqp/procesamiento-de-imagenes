from Procesamiento import Procesamiento
from sys import argv
import time

abrir = False # para abrirla en una ventana la imagen obtenida

def main(nombreImagen, RANGO):
	
	pro = Procesamiento(nombreImagen) # instanciamos
	# grises
	grises = pro.aplicarGris(abrir)  
	# sumar filas de la imagen
	sumaHorizontales = pro.sumarFilas()
	# sumar columna de la imagen
	sumaVerticales = pro.sumarColumnas()
	# graficar
	#pro.graficar(sumaHorizontales, sumaVerticales)
	# minimos locales
	lineasVerticales = pro.minimosLocales(sumaVerticales)
	lineasHorizontales = pro. minimosLocales(sumaHorizontales)
	# dibujamos la lineas de los minimos locales
	(lineasHorizontales, lineasVerticales) = pro.linasImaginarias(lineasHorizontales, lineasVerticales)
	# dibujamos los puntos en donde cruzan las lineas imaginarias
	pro.setImagen("salidaGRIS.png")
	pixelesCruz = pro.calcularCruces(lineasVerticales, lineasHorizontales)

	# filtro
	pro.setImagen(nombreImagen) # receteamos
	pro.aplicarFiltro(abrir) 
	# convolucion
	pro.setImagen("salidaFILTRO.png") # imagen base
	pro.aplicarConvolucion(abrir) 
	# normalizacion
	pro.setImagen("salidaCONVOLUCION.png") # imagen base
	pro.aplicarNormalizacion(abrir) 
	# binarizacion
	pro.setImagen("salidaNORMALIZACION.png") # imagen base
	pro.aplicarBinarizacion(abrir, RANGO) 
	# buscar objetos y centro masa
	pro.setImagen("salidaBINARIZADA.png") # receteamos
	pro.buscarObjetos(abrir, pixelesCruz) # BFS
	
	

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen
# argv[2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(argv[1], int(argv[2]))


