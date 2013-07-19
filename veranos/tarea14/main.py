import sys

from Gif import Gif
from Imagen import Imagen
from AdministradorImagen import AdministradorImagen
from Comparador import Comparador

def main(nombreGif):
	# leer el gif y obtener sus imagenes
	g = Gif() # instanciamos
	imagenes = g.readGif(nombreGif)

	# por cada imagen crear un objeto
	objetosImagenes = list()
	for id_,v in enumerate(imagenes):
		ima = Imagen(v, id_+1)
		objetosImagenes.append(ima)

	ad = AdministradorImagen()
	co = Comparador()
	for i,oi in enumerate(objetosImagenes):
		# los resultados de este metodo se sustituyen por 
		# el atributo bordes de cada imagen
		print 'Buscando objetos en la imagen', str(i+1)+'/'+str(len(imagenes))
		ad.buscarObjetos(oi, pixel='blanco') # buscara pixeles blancos o negros
		co.eliminarMarco(oi)
		if i>0: # para empezar desde la segunda imagen
			co.analizis(objetosImagenes[i-1], objetosImagenes[i])



	g.createGif() # creamos el gif con las imagenes resultantes








######### Parametros del programa ### 
# [1] - nombre del gif
#####################################
main(sys.argv[1])



