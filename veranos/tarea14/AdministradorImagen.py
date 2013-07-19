import Image
import numpy
import math
import random

# sobel
mascaraX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
mascaraY = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

def obtenerVecinos(x, y, ancho, alto, pixeles):
  '''
    Recibe el pixel actual(x,y), las dimensiones de la imagen y
      los pixeles de la imagen de la cual obtenemos los vecinos.
      Regresa una matriz de 3*3 con los vecinos del pixel, en caso
      de no tener un vecino el campo se llena(por default) con cero.
  '''
  vecindad = numpy.zeros((3,3))
  for my in range(y-1, y+2):
    for mx in range(x-1, x+2):        
      if mx >= 0 and my >= 0 and mx < ancho and my < alto:
        # asignamos el vecino a la matriz
        vecindad[mx-(x-1), my-(y-1)] = pixeles[mx, my][1] 
  return vecindad


class AdministradorImagen(object):
	def convolucion(self, imagen, mascara, mascara2=[]):
		''' Este metodo recibe un OBJETO tipo imagen y aplica convolucion
		en una imagen nueva. Para que la original no se modifique. '''


		w = imagen.w
		h = imagen.h
		pixOriginales = imagen.pixeles

		# creamos una nueva imagen para no modificar la imagen original
		nuevaImagen = Image.new("RGB", (w, h))
		newPixeles = nuevaImagen.load() 
		
		if not mascara2: # recibe una sola mascara
			for x in range(w):
				for y in range(h):
					R = G = B = 0
					# obtenemos todos los vecinos de pixel actual
					for mx in xrange(x-1, x+2):
						for my in xrange(y-1, y+2):
							if mx>=0 and my>=0 and mx<w and my<h:
								R += mascara[mx - (x-1)][my - (y-1)] * pixOriginales[mx, my][0]
								G += mascara[mx - (x-1)][my - (y-1)] * pixOriginales[mx, my][1]
								B += mascara[mx - (x-1)][my - (y-1)] * pixOriginales[mx, my][2]
					newPixeles[x, y] = (R, G, B)
		else:
			for x in range(w):
				for y in range(h):
					# obtenemos todos los vecinos de pixel actual
					vecindad = obtenerVecinos(x, y, w, h, pixOriginales)
					gx = sum(sum(vecindad * mascara)) # multiplicamos matrices para obtener los gradientes en x
					gy = sum(sum(vecindad * mascara2)) # multiplicamos matrices para obtener los gradientes en y

					xm = (gx ** 2) # pitagoras
					ym = (gy ** 2) # pitagoras
					nuevoPixel = int(math.sqrt(xm + ym)) # pitagoras

					if nuevoPixel > 255:
						nuevoPixel = 255
					if nuevoPixel < 0:
						nuevoPixel = 0

					newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel) 

		#nuevaImagen.show() # mostramos en ventana
		#nuevaImagen.save('SalidaConvolucion.png') # guardamos el archivo    
		return nuevaImagen

	
	def binarizacion(self, imagenBase, RANGO):
	    ''' Este metodo recibe una imagen y aplica binarizacion. El rango es
	    un valor que mientras mas se acerque a 255(sin pasarlo) 
	    se obtendra bordes mas gruesos.
	    '''

	    w = imagenBase.size[0]
	    h = imagenBase.size[1]
	    pixelesBase = imagenBase.load() # cargamos los pixeles de la imagen base

	    # creamos una copia para no modificar la imagen original
	    nuevaImagen = Image.new('RGB', (w, h))
	    newPixeles = nuevaImagen.load() 

	    for x in range(w):
	      for y in range(h):
	        # 0 = NEGRO || 255 = BLANCO
	        nuevoPixel = (0, 255)[min(pixelesBase[x,y]) > RANGO] # operador ternario
	        newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)       
	    
	    #nuevaImagen.show() # mostramos en ventana
	    #nuevaImagen.save('SalidaBinarizacion.png') # guardamos el archivo
	    return nuevaImagen


	def buscarObjetos(self, obImagenBase, pixel='negro'):
		''' Este metodo recibe un objeto tipo 'Imagen' y sobre el se aplica
		convolucion y binarizacion, con estos filtro se buscan objetos '''
		
		# se aplican filtros....
		conv = self.convolucion(obImagenBase, mascaraX, mascaraY)
		bina = self.binarizacion(conv, RANGO=100)

		# como este metodo se llama varias veces hay que asegurarnos que
		# la lista de bordes este vacia en caso contrario vaciarla
		if obImagenBase.bordes: 
			obImagenBase.bordes = list() # la lista contiene algo. La reiniciamos

		w = obImagenBase.w
		h = obImagenBase.h
		pixOriginales = obImagenBase.pixeles

		imagenCopia = bina.copy()
		tempPix = imagenCopia.load() 

		# 0 = negro || 255 = blanco
		if pixel == 'blanco': # pixel a buscar
			objeto = (255, 255, 255) 
		else: 
			objeto = (0, 0, 0) 

		pixelesCola = list()
		pixelesVisitados = dict()

		for x in range(w): # cliclo principal
			for y in range(h): # ciclo principal
				# buscamos el primer pixel para agregarlo como candidato
				if objeto == tempPix[x,y]:
					pixelesCola.append((x,y)) # agregamos el candidato a la cola

					masa = list() # el objeto que se forma con el candidato
					while pixelesCola > 0: 
						try:
							pixelesActual = pixelesCola[0] # asignos el candidato a analizar
							pixelesVisitados[x, y] = True # agreamos a visitados
						except:
							break # ya no hay elementos
						# recorremos sus vecinos
						for mx in range(pixelesActual[0]-1, pixelesActual[0]+2):
							for my in range(pixelesActual[1]-1, pixelesActual[1]+2):			
								# aseguramos que sea igual al objeto a buscar, que no este 
								# en la cola y que no se haya visitado mas aparte que no salga 
								# de las dimensiones de la imagen
								if mx>=0 and my>=0 and mx<w and my<h\
								   and tempPix[mx, my] == objeto\
								     and (mx, my) not in pixelesCola\
								      and not pixelesVisitados.has_key((mx, my)):
								    pixelesCola.append((mx, my)) #agreamos el vecino a la cola
								    pixelesVisitados[mx, my] = True # agreamos visitados
						masa.append(pixelesCola.pop(0)) # borramos el candidato analizado
					
					obImagenBase.bordes.append(masa)     # chicas y el fondo


				
					nuevoColor = random.randrange(0,255) # chicas y el fondo
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos
						tempPix[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)

		#imagenCopia.show() # mostramos en ventana
		#imagenCopia.save('SalidaObjetos.png') # guardamos el archivo









