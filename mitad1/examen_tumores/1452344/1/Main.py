from Procesamiento import Procesamiento
from sys import argv

abrir = False # para abrirla en una ventana la imagen obtenida

def main(nombreImagen, RANGO):

	pro = Procesamiento(nombreImagen)
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
	# buscar tumores y centro masa
	pro.setImagen("salidaBINARIZADA.png") # receteamos
	pro.buscarTumores(abrir) 

		
###### CALCULO DE TUMORES BASE A DIMENSIONES ######

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen
########################################
main(argv[1], 15)


