from Procesamiento import Procesamiento
from sys import argv

abrir = False # para abrirla en una ventana la imagen obtenida

def main(nombreImagen, RANGO):
	pro = Procesamiento(nombreImagen) # instanciamos
	# filtro
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
	# buscar objetos tipo borde
	pro.setImagen("salidaBINARIZADA.png") # receteamos
	figuras = pro.buscarObjetosTipoBorde(abrir) # BFS
	# dibujamos la tangente de cada figura detectada
	pro.setImagen("salidaOBJETOS.png")
	puntosInterseccionMedio = pro.dibujarTangente(abrir, figuras)
	# votacion por el centro
	pro.setImagen("salidaOBJETOS.png")
	pro.votacionPixeles(abrir, puntosInterseccionMedio)

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen
# argv[2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(argv[1], int(argv[2]))


