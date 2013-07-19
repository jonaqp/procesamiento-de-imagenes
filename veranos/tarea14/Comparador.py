import Image, ImageDraw

numero = 0

class Comparador(object):
	def eliminarMarco(self, objetoImagen):
		objetoImagen.bordes = objetoImagen.bordes[1:] # eliminamos el marco de la imagen

	def contarMasas(self, objetoImagen):		
		print len(objetoImagen.bordes)
		return len(objetoImagen.bordes)

	def obtenerPuntoMedio(self, masa, masa2):
		# Recibe masas(lista de pixeles que forman el borde de una figura) 
		# y en el busca sus coordenadas minimas/maximas en eje x, eje y

		# para masa 1
		minX = minY = 10000
		maxX = maxY = 0

		# para masa 2
		minX2 = minY2 = 10000
		maxX2 = maxY2 = 0

		# recorremos el objeto que queremos encerrar
		for (x,y) in masa:
			if x < minX:
				minX = x
			if x > maxX:
				maxX = x
			if y < minY:
				minY = y
			if y > maxY:
				maxY = y

		for (x2,y2) in masa2:
			if x2 < minX2:
				minX2 = x2
			if x2 > maxX2:
				maxX2 = x2
			if y2 < minY2:
				minY2 = y2
			if y2 > maxY2:
				maxY2 = y2

		centro = (minX+maxX)/2, (minY+maxY)/2 # centro del objeto
		centro2 = (minX2+maxX2)/2, (minY2+maxY2)/2 # centro del objeto

		return centro, centro2	

	def direccion(self, imagenAnterior, imagenActual):
		# obtenemos los puntos medios de cada figura en las imagenes y hacemos
		# una diferencia
		
		for masa, masa2 in zip(imagenAnterior.bordes, imagenActual.bordes):
			dir_ = list()
			# buscamos el punto centro de cada masa
			(centro, centro2) = self.obtenerPuntoMedio(masa, masa2)
			# restamos centros
			if centro2[0] > centro[0]:
				# se movio en X hacia la derecha
				print 'Derecha',
				dir_.append('Der')
			else:
				# se movio en X hacia la izquierda
				print 'Izquierda',
				dir_.append('Izq')
			if centro2[0] == centro[0]:
				print 'No se movio en X'
				dir_.append('NO_X')			

			if centro2[1] > centro[1]:
				# se movio en Y hacia abajo
				print 'y abajo'
				dir_.append('Aba')
			else: 
				# se movio en Y hacia arriba
				print 'y arriba'
				dir_.append('Arr')
			if centro2[1] == centro[1]:
				print 'No se movio en Y'
				dir_.append('NO_Y')

		return dir_
				


	def mostrarResultados(self, imagenActual, mensaje):		
		global numero
				# direccion en x       # direccion en Y
		mensaje = mensaje[0]      +'-'+    mensaje[1]

		# creamos una nueva imagen para no modificar la imagen original
		nuevaImagen = Image.new("RGB", (imagenActual.w, imagenActual.h))
		newPixeles = nuevaImagen.load() 

		draw = ImageDraw.Draw(nuevaImagen) # creamos un objeto para dibujar

		# hacer una copia de la imagen actual a la nueva creada
		for y in range(imagenActual.h):
			for x in range(imagenActual.w):
				newPixeles[x,y] = imagenActual.pixeles[x,y]

		# pintar el pantalla hacia donde se movio y guardar imagen
		
		draw.text((10, 10), mensaje, fill="green")
		nuevaImagen.show()
		nuevaImagen.save(str(numero+1)+'.png')
		numero += 1


	def analizis(self, imagenAnterior, imagenActual):
		''' Este metodo recibe 2 objetos de imagen '''
		# primero contamos las masas de cada imagen
		# si la imagen anterior tiene la misma cantidad de masas que la imagen 
		# actual, significa que solo hubo un movimiento
		if len(imagenActual.bordes) > 0:		
			if len(imagenAnterior.bordes) == len(imagenActual.bordes):
				# buscamos la direccion del movimiento
				dir_ = self.direccion(imagenAnterior, imagenActual)
			else:
				print 'Otro'
		else: 
			print 'La imagen', imagenActual.id, 'no tiene ninguna figura'
			print 'Masas detectadas', len(imagenActual.bordes)
			print 'contra', len(imagenAnterior.bordes)

		self.mostrarResultados(imagenActual, dir_)











