from TumoresPulmon import TumoresPulmon
import sys, time

abrir = False # para abrirla en una ventana la imagen obtenida

def main(nombreImagen, RANGO):

	pro = TumoresPulmon(nombreImagen)
	# filtro
	pro.aplicarFiltro(abrir) 
	
	# convolucion
	inicio = time.time()
	pro.setImagen("salidaFILTRO.png") # imagen base
	pro.aplicarConvolucion(abrir) 
	print "tiempo final", time.time() - inicio

	# normalizacion
	pro.setImagen("salidaCONVOLUCION.png") # imagen base
	pro.aplicarNormalizacion(abrir) 
	# binarizacion
	pro.setImagen("salidaNORMALIZACION.png") # imagen base
	pro.aplicarBinarizacion(abrir, RANGO) 
	# hacemos los bordes mas gruesos
	pro.setImagen("salidaBINARIZADA.png") # receteamos
	pro.engordarBordes(abrir)

	# buscar tumores y centro masa
	#pro.setImagen("salidaBINARIZADA.png") # receteamos
	#pro.buscarTumores(abrir) 


		
###### CALCULO DE TUMORES BASE A DIMENSIONES ######

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen
########################################
main(sys.argv[1], int(sys.argv[2]))


