import Image, ImageDraw
import sys
import numpy
import math
import random

from Picture import Picture
from Tamano import Tamano


ABRIR = False # bandera para abrir una ventana con los resultados de las pruebas

def sobel():
  '''Mascara de convolucion: Sobel. '''
  return ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], \
      [[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

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


class PictureManage(object):
	def __init__(self, imagen):
		self.obPic = imagen
		self._objetos = list()  # esta lista puede contener objetos formados por
								# pixeles negro o blancos, dependiendo del metodo
								# buscarObjetos.

	def convolucion(self, mascara, mascara2=[]):
		print 'Aplicando convolucion sobre la imagen original...'

		w = self.obPic.w
		h = self.obPic.h
		pixOriginales = self.obPic.pixeles

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

		if ABRIR:
			nuevaImagen.show() # mostramos en ventana
		nuevaImagen.save('SalidaConvolucion.png') # guardamos el archivo    
		print 'LISTO'
		return nuevaImagen

	def binarizacion(self, imagenBase, RANGO):
	    print 'Aplicando binarizacion...'

	    w = self.obPic.w
	    h = self.obPic.h

	    pixelesBase = imagenBase.load() # cargamos los pixeles de la imagen base

	    # creamos una copia para no modificar la imagen original
	    nuevaImagen = Image.new('RGB', (w, h))
	    newPixeles = nuevaImagen.load() 

	    for x in range(w):
	      for y in range(h):
	        # 0 = NEGRO || 255 = BLANCO
	        nuevoPixel = (0, 255)[min(pixelesBase[x,y]) > RANGO] # operador ternario
	        newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)       
	    
	    if ABRIR:
	    	nuevaImagen.show() # mostramos en ventana
	    nuevaImagen.save('SalidaBinarizacion.png') # guardamos el archivo
	    print 'LISTO' 
	    return nuevaImagen

	def buscarObjetos(self, imagenBase, pixel='negro'):
		print 'Buscando objetos...'

		# como este metodo se llama varias veces hay que asegurarnos que
		# la lista ._objetos este vacia en caso contrario vaciarla
		if self._objetos: 
			self._objetos = list() # la lista contiene algo. La reiniciamos

		w = self.obPic.w
		h = self.obPic.h
		pixOriginales = self.obPic.pixeles

		imagenCopia = imagenBase.copy()
		tempPix = imagenCopia.load() 

		# 0 = negro || 255 = blanco
		if pixel == 'blanco': # pixel a buscar
			objeto = (255, 255, 255) 
		else: 
			objeto = (0, 0, 0) 

		print '    Buscando pixeles', pixel +'s'

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
					self._objetos.append(masa)

					
					nuevoColor = random.randrange(0,255)
					nuevoColor2 = random.randrange(0,255)
					nuevoColor3 = random.randrange(0,255)
					for pixel in masa: # pintamos
						tempPix[pixel] = (nuevoColor, nuevoColor2, nuevoColor3)

		if ABRIR:
			imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaObjetos.png') # guardamos el archivo
		print 'LISTO'

	def pintarVecinos(self, x, y, pixelesCopia, color=(255,0,0)):
		for mx in range(x-1,x+2):
			for my in range(y-1,y+2):
				if mx>=0 and my>=0 and mx<self.obPic.w and my<self.obPic.h:
					pixelesCopia[mx,my] = color

	def esquinas(self, imagenBase):
		print 'Detectando esquinas...'

		w = self.obPic.w
		h = self.obPic.h
		pixOriginales = self.obPic.pixeles

		pixelesBase = imagenBase.load() # cargamos los pixeles de la imagen base

		# creamos una copia para no modificar la imagen original
		imagenCopia = imagenBase.copy()
		pixelesCopia = imagenCopia.load() 	

		# lista que contendra los pixeles tipo esquina
		pixelesEsquinas = list()
		for x in range(w):
			for y in range(h):
				vecindad = list()
				for mx in range(x-1,x+2):
					for my in range(y-1,y+2):
						if mx>=0 and my>=0 and mx<w and my<h:
							vecindad.append(pixelesBase[mx, my][0])

				vecindad.sort()
				z = vecindad[len(vecindad)/2]

				if(z - pixelesBase[x,y][1]) != 0:
					self.pintarVecinos(x, y, pixelesCopia)
					pixelesEsquinas.append((x,y))

		if ABRIR:
			imagenCopia.show()
		imagenCopia.save('SalidaEsquinas.png')
		print 'LISTO'  
		return pixelesEsquinas


	def engordarBorde(self, imagenBase, nivel):
		''' 
			Esta funcion recibe una imagen y engorda sus bordes 
			segun el nivel, el valor del nivel debe estar entre 1 y 3.
		'''
		# capturamos el error en la "capa 8"
		if nivel < 1:
			nivel = 1
		if nivel > 3:
			nivel = 3

		print 'Engordando pixeles...'
		print '     NIVEL', nivel

		w = self.obPic.w
		h = self.obPic.h
		
		# cargamos la imagen base
		#temp = Image.open('SalidaBinarizacion.png')
		tempPix = imagenBase.load() # cargamos sus pixeles

		# y hacemos una copia para que no se modifique
		imagenCopia = imagenBase.copy()
		pixelesCopia = imagenCopia.load()

		
		# recorremos los pixeles de vecino
		for bor in self._objetos:
			for x,y in bor:
				# buscamos sus vecinos y si tiene 3 o mas que sean negros,
				# significa que es un pixel que podemos engordar
				vecindad = obtenerVecinos(x, y, w, h, tempPix)
				
				negros = [vecindad[a,b] for a in range(3)
											for b in range(3)
												if vecindad[a,b] == 0.0]

				if len(negros) >= 3:
					for j in range(y-nivel, y+(nivel+1)): 
						for i in range(x-nivel, x+(nivel+1)):
							if i>=0 and j>=0 and i<w and j<h:
								pixelesCopia[i, j] = (255, 255, 255)

		if ABRIR:
			imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaBorde.png')
		print 'LISTO'
		return imagenCopia


	def cajaEnvolvente(self, objeto, imagen, mensaje=''):
		# Recibe un objeto y en el busca sus coordenadas minimas/maximas en eje x, eje y

		w = self.obPic.w
		h = self.obPic.h
		pixOriginales = self.obPic.pixeles

		draw = ImageDraw.Draw(imagen) # creamos un objeto para dibujar

		minX = w
		maxX = 0
		minY = h
		maxY = 0

		# recorremos el objeto que queremos encerrar
		for x,y in objeto:	
			if x < minX:
				minX = x
			if x > maxX:
				maxX = x
			if y < minY:
				minY = y
			if y > maxY:
				maxY = y

		# descartamos aquellos objetos que sean muy chicos
		if minX < maxX and minY < maxY: 
			if not mensaje:
				# encerramos en un cuadrado el objeto recibido como parametro
				draw.rectangle(((minX, minY), (maxX, maxY)), outline="red")
			else:
				# escribimos en el punto centro del objeto el mensaje recibido como parametro
				puntoCentro = (minX+maxX)/2, (minY+maxY)/2 # centro del objeto
				draw.text(puntoCentro, mensaje, fill="green")

	def clasificarPoligono(self, objeto, imagen):
		# recorremos la figura en busca de sus angulos

		
		return '4'


	def detectarPoligonos(self, imagenBase, pixelesEsquinas):
		figuras = {3:'Tri', 4:'Cua', 5:'Pen', 6:'Hex', 'mas':'6+'} 
		poligonos = list() # guarda las poligonos detectados

		# creamos una copia para no modificar la imagen original
		imagenCopia = imagenBase.copy()
		pixelesCopia = imagenCopia.load() 
		
		# Algoritmo:
		# recorremos la imagen  y los pixeles tipo esquina
		# el algoritmo trata de recorrer los bordes por figura y si el borde se topa con 
		# mas de 3 esquinas significa que es un poligono.

		# recorremos los objetos detectados
		self._objetos = self._objetos[1:] # eliminamos el marco de la imagen
		for objeto in self._objetos:
			lado = 0
			for pixel in objeto:
				if pixel in pixelesEsquinas:
					lado += 1
					self.pintarVecinos(pixel[0], pixel[1], pixelesCopia)
			
			if lado in figuras:
				self.cajaEnvolvente(objeto, imagenCopia, figuras[lado])
				poligonos.append(objeto)
			elif lado>6: # tiene mas de 6 lados
				self.cajaEnvolvente(objeto, imagenCopia, figuras['mas'])
				poligonos.append(objeto)
			


		if ABRIR:
			imagenCopia.show() # mostramos en ventana
		imagenCopia.save('SalidaPoligonos.png') # guardamos el archivo
		print 'Detectando poligonos...'
		print 'LISTO'
		return(poligonos, imagenCopia)


	def dibujarCirculos(self, imagenBase, cordenadas, radio):
		umbral = 2

		w = self.obPic.w
		h = self.obPic.h

		pixlesBase = imagenBase.load()

		draw = ImageDraw.Draw(self.obPic.imReducida)

		for x, y in cordenadas:
			v1 = v2 = v3 = v4 = False
			for k in range(-umbral, umbral):
				curr_radio = radio+k

				if (x+curr_radio)<w and (x+curr_radio)>0 and (x-curr_radio)<w and (x-curr_radio)>0:

					if pixlesBase[x+curr_radio, y] != (0, 0, 0):
						v1 = True

					if pixlesBase[x-curr_radio, y] != (0, 0, 0):
						v2 = True

				if (y+curr_radio)<h and (y+curr_radio)>0 and (y-curr_radio)<h and  (y-curr_radio)>0:
					if pixlesBase[x, y+curr_radio] != (0, 0, 0):
						v3 = True

					if pixlesBase[x, y-curr_radio] != (0, 0, 0):
						v4 = True

					if v1 and v2 and v3 and v4:
						draw.text((x, y), 'Cir', fill="green")
						draw.ellipse((x-radio, y-radio, x+radio, y+radio), outline ='red')
						print '    * circulo con radio', radio    
						break
		self.obPic.imReducida.save('SalidaPoligonos.png')


	def zeros(self, n, m):
		matrix = []
		for i in range(n):
			tmp = []
			for j in range(m):
				tmp.append(0)
			matrix.append(tmp)
		return matrix


	def votacionPixeles(self, votos, (ancho, alto)):
		dim = max(ancho, alto)
		for rango in range(1, int(round(dim*0.1))):
			agregado = True
			while agregado:
				agregado = False
				for x in range(ancho):
					for y in range(alto):
						v = votos[x][y]
						if v > 0:
							for n in range(-rango, rango):
								for m in range(-rango, rango):
									if not (n==0 and m==0):
										if (x+m)>=0 and (x+m)<ancho and (y+n)>=0 and (y+n)<alto:
											v2 = votos[x+m][y+n]
											if v2 > 0:
												if (v-rango)>=v2:
													votos[x][y] = v+v2 
													votos[x+m][y+n] = 0
													agregado = True
		return votos

	def buscarCentros(self, radio, imaGradienteX, imaGradienteY):
		pixelesGx = imaGradienteX.load()
		pixelesGy = imaGradienteY.load()

		w = self.obPic.w
		h = self.obPic.h

		votos = self.zeros(w, h)

		for x in range(w):
			for y in range(h):
				if pixelesGy[x, y]!=(0, 0, 0) or pixelesGx[x, y]!=(0, 0, 0):
					(R, G, B) = pixelesGx[x, y] # pixel actual en gx
					gx = (R+G+B)/3  
					(R, G, B) = pixelesGy[x, y] # pixel actual en gy
					gy = (R+G+B)/3 
					g = math.sqrt(gx ** 2 + gy ** 2) # pitagoras

					if abs(g) > 0: 
						theta = math.atan2(gy , gx)
						centroX = int(round(x - radio * math.cos(theta+math.radians(90.0))))
						centroY = int(round(y - radio * math.sin(theta+math.radians(90.0))))
						if centroX>=0 and centroX<w and centroY>=0 and centroY<h:
							votos[centroX][centroY] += 1

		votos = self.votacionPixeles(votos, (w, h))

		maximo = 0
		suma = 0.0
		for x in range(w):
			for y in range(h):
				v = votos[x][y]
				suma += v
				if v>maximo:
					maximo = v

		promedio = suma / (w*h)
		umbral = (maximo+promedio) / 2.0

		cordenadas = []
		for x in range(w):
			for y in range(h):
				v = votos[x][y]
				if v>umbral:
					cordenadas.append((x, y))
		return cordenadas

	def detectarCirculos(self, imagenBase, imaGradienteX, imaGradienteY, salto=3):
	    print 'Detectando circulos radio desconocido...'
	    
	    w = self.obPic.w
	    h = self.obPic.h

	    radioMinimo = 6
	    radioMaximo = int((w**2 + h**2)**0.5*0.5)

	    print '    Radio minimo:', radioMinimo
	    print '    Radio maximo:', radioMaximo
	    print '    Con salto de:', salto, 'pixeles'

	    # hacemos el recorrido por todos los radios posibles
	    for radio in range(radioMinimo, radioMaximo, salto):
	      coordenadas = self.buscarCentros(radio, imaGradienteX, imaGradienteY)
	      self.dibujarCirculos(imagenBase, coordenadas, radio)

	    print 'LISTO'


def main(nombreImagen, rangoBinarizacion):
	print 'Julio 2013: Osvaldo Hinojosa'

	im = Picture(nombreImagen) # obtenemos las caracteristicas de la imagen
	
	# si la imagen supera los 300 pixeles de ancho o alto la redimensionamos
	# para mayor velocidad
	REDUCIR = False
	new_w = im.w
	new_h = im.h
	while new_w > 300 or new_h > 300: # calculamos el nuevo ancho
		new_w = new_w/2
		new_h = new_h/2
		REDUCIR = True
	if REDUCIR:
		ta = Tamano(im)
		imagenReducida = ta.redimensionar(new_w, new_h)
		# sustituimos a los nuevos valores
		im.w = new_w
		im.h = new_h
		im.pixeles = imagenReducida.load()

	
	pm = PictureManage(im) # jugamos con la imagen
	mascaraX, mascaraY = sobel() # cargamos la mascara, tiene que ser de 3x3

	# aplicar convolucion para gx
	imaGradienteX = pm.convolucion(mascaraX)
	# aplicar convolucion para gy
	imaGradienteY = pm.convolucion(mascaraY) 
	# aplicamos convolucion
	imaConvolucion = pm.convolucion(mascaraX, mascaraY)
	
	# aplicamos binarizacion
	imaBinarizacion = pm.binarizacion(imaConvolucion, rangoBinarizacion)
	
	# detectar objetos
	# pixel = de que color son los objetos a buscar
	# 'blanco' = bordes || 'negro' = cosas que no sean bordes
	pm.buscarObjetos(imaBinarizacion, pixel='blanco') # le mandamos la imagen 
													  # y el color del pixel a buscar
		
	# detectamos las esquinas de la imagen
	pixelesEsquinas = pm.esquinas(imaBinarizacion)
	
	# engordamos pixeles de toda la imagen, el valor del nivel debe ser 1, 2 o 3.
	imagenBorde = pm.engordarBorde(imaBinarizacion, nivel=1)

	# volvemos a encontrar objetos, ahora con los bordes mas gruesos
	# esto para que la lista de '._objetos' se actualize y detectar poligonos
	# puedar correr sin problemas.
	pm.buscarObjetos(imagenBorde, pixel='blanco')

	# detectar poligonos
	poligonos, imaPoligonos = pm.detectarPoligonos(imaBinarizacion, pixelesEsquinas)
	
	im.imReducida = imaPoligonos # se sustituye el valor de la imagen copia
								 # esta trae las nuevas dimensiones.
								 # Es necesario en el metodo 'dibujarCirculos()'
	
	# detectar cosas redondas de los objetos que no fueron poligonos
	pm.detectarCirculos(imaPoligonos, imaGradienteX, imaGradienteY)
	
	# distigir entre eclipses y circulos
	''' PENDIENTE '''


######## Parametros del programa ########
# [1] = (string) nombre de la imagen
# [2] = (int) rango de binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
#########################################
main(sys.argv[1], int(sys.argv[2]))