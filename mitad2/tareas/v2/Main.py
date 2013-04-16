from Procesamiento import Procesamiento
from Lineas import Lineas
from Circulo import Circulo
from sys import argv

abrir = False # para abrirla en una ventana la imagen obtenida

def main(nombreImagen, RANGO):
	# -------------- SABADO -------------------- # 
	pro = Procesamiento(nombreImagen) # instanciamos
	# grises
	grises = pro.aplicarGris(abrir) 
	# umbral
	pro.setImagen(nombreImagen) # receteamos
	pro.aplicarUmbral(abrir) 
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
	pro.buscarObjetos(abrir) 
	
	# -------------- LINEAS --------------------- #
	# detectar lineas rectas
	lin = Lineas(nombreImagen) # instanciamos
	lin.detectarLineas(abrir)

	# ------------- CIRCULO --------------------- #
	# detectar circulos radio conocido
	#cir = Circulo(nombreImagen)
	#cir.detectarCirculos(abrir) 
	# detectar circulos radio conocido
	#cir = Circulo(nombreImagen) # PENDIENTE
	#cir.detectarCirculosDesconocidos(abrir) # pendiente

	

######## PARAMATROS DEL PROGRAMA #######
# argv[1] =(string) nombre de la imagen
# argv[2] =(int) rango binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(argv[1], int(argv[2]))


