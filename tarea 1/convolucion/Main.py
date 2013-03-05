from Datos import Datos
from Procesamiento import Procesamiento
from Imagen import Imagen

from sys import argv
import time
from Tkinter import *


def main(nombreImagen):
	# objeto imagen
	ima = Imagen(nombreImagen)
	(pixeles, ancho, alto) = ima.lectura()
	# objetos datos
	#dat = Datos()
	#RANGO_BINARIZACION = dat.convolucion(argv)
	# objeto del procesamiento
	pro = Procesamiento(pixeles, ancho, alto)
	# tiempoFiltroInicio = time.time()
	# tiempoFiltroFinal = time.time()

	# convertimos a grises
	#imagenGris = pro.convertirGris()
	#ima.setNombreImagen("salidaGRIS.png") # nuevo nombre para guardar archivo
	#ima.guardar(imagenGris, ancho, alto) # guardamos

	# aplicar filtro
	#imagenFiltro = pro.aplicarFiltro() # (que se vea borrosa)
	#ima.setNombreImagen("salidaFILTRO.png") # nuevo nombre para guardar archivo
	#ima.guardar(imagenFiltro, ancho, alto) # guardamos

	# aplicar convolucion
	#imagenConvolucion = pro.aplicarConvolucion() # detectar bordes
	#ima.setNombreImagen("salidaCONVO.png")  # nuevo nombre para guardar archivo
	#ima.guardar(imagenConvolucion, ancho, alto) # guardamos

	# aplciar normalizacion
	#imagenNormalizada = pro.aplicarNormalizacion(imagenConvolucion)
	#ima.setNombreImagen("salidaNORMA.png")  # nuevo nombre para guardar archivo
	#ima.guardar(imagenNormalizada, ancho, alto) # guardamos	

	# aplicar binarizacion
	#(imagenBinarizada, pixelesVisitar) = pro.aplicarBinarizacion(imagenNormalizada, RANGO_BINARIZACION)
	#ima.setNombreImagen("salidaBINA.png")  # nuevo nombre para guardar archivo
	#ima.guardar(imagenBinarizada, ancho, alto) # guardamos	
	
	# buscamos objetos
	#imagenObjetos, (etiquetas) = pro.buscarObjetos(imagenBinarizada, pixelesVisitar)
	#ima.setNombreImagen("salidaOBJETOS.png")  # nuevo nombre para guardar archivo
	#ima.guardarEtiquetas(imagenObjetos, ancho, alto, etiquetas) # guardamos	

	#lineDetect = pro.detectarLineas()
	#ima.setNombreImagen("salidaLINEAS.png")  # nuevo nombre para guardar archivo
	#ima.guardar(lineDetect, ancho, alto) # guardamos

	circuloDetect = pro.detectarCirculo()
	ima.setNombreImagen("salidaCIRCULO.png")  # nuevo nombre para guardar archivo
	ima.guardar(circuloDetect, ancho, alto) # guardamos


	

	return

main(argv[1])