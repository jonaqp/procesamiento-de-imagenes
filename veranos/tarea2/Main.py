from Procesamiento import Procesamiento
from sys import argv

abrir = True # para abrirla en una ventana la imagen obtenida

def main(nombreImagen):
	pro = Procesamiento(nombreImagen) # instanciamos
	
	# filtro
	pro.setImagen(nombreImagen) # receteamos
	pro.aplicarFiltro(abrir) 

	# normalizacion
	pro.setImagen("salidaFILTRO.png") # imagen base
	pro.normalizar(abrir, 'sobel') # receteamos

	pro.setImagen("salidaFILTRO.png") # imagen base
	pro.normalizar(abrir, 'roberts') # receteamos
	
	pro.setImagen("salidaFILTRO.png") # imagen base
	pro.normalizar(abrir, 'prewitt') # receteamos

	

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen con extension
########################################
main(argv[1])


