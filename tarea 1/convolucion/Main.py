from Datos import Datos
from Grises import Grises
from ProceImagen import ProceImagen
from Filtro import Filtro

from sys import argv
import time
from Tkinter import *


def main(nombreImagen):
	# objetos
	ima = ProceImagen(nombreImagen)
	(pixeles, ancho, alto) = ima.lectura()

	# convertir a grices
	tiempoGrisesInicio = time.time()
	gri = Grises(pixeles)
	imagenGris = gri.convertir()
	ima.guardar(pixeles, ancho, alto)
	tiempoGrisesInicio = time.time()

	# aplicar filtro
	imaFiltro = ProceImagen("salidaFILTRO.png")
	tiempoFiltroInicio = time.time()
	fil = Filtro(pixeles, ancho)
	imagenFiltro = fil.aplicar() # aplicamos FILTRO(que se vea borrosa)
	imaFiltro.guardar(imagenFiltro, ancho, alto) # guardamos
	tiempoFiltroFinal = time.time()

	# aplicar diferenciacion
	imaDifere = ProceImagen("salidaDIFERENCIACION.png")
	tiempoDiferenciacionInicio = time.time()
	dif = Diferenciacion(imagenGris, imagenFiltro)
	imagenDiferenciacion = dif.aplicar() # detectar bordes
	imaDifere.guardar(imagenDiferenciacion, ancho, alto, "salidaDIFERENCIACION.png") 
	tiempoDiferenciacionFinal = time.time()


	return

main(argv[1])