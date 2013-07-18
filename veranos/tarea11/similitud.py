import Image
import ImageDraw
import sys
import math
import numpy
import random

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

class Imagen(object):
  def __init__(self, nombreImagen):
    self.imagen = Image.open(nombreImagen)
    self.pixeles = self.imagen.load()
    self.ancho = self.imagen.size[0]
    self.alto = self.imagen.size[1]
    print self.imagen.format, self.imagen.size, self.imagen.mode

class AdministradorImagen(object):
  def __init__(self, imagen):
    self.obIma = imagen
    self._objetos = list()

  def aplicarConvolucion(self, mascara, mascara2=[]):
    print 'Aplicando convolucion sobre la imagen original...'

    # creamos una nueva imagen para no modificar la imagen original
    nuevaImagen = Image.new("RGB", (self.obIma.ancho, self.obIma.alto))
    newPixeles = nuevaImagen.load() 

    if not mascara2: # recive una sola mascara
      for x in range(self.obIma.ancho):
        for y in range(self.obIma.alto):
          R = G = B = 0
          # obtenemos todos los vecinos de pixel actual
          for mx in xrange(x-1, x+2):
            for my in xrange(y-1, y+2):
              if mx>=0 and my>=0 and mx<self.obIma.ancho and my<self.obIma.alto:
                R += mascara[mx - (x-1)][my - (y-1)] * self.obIma.pixeles[mx, my][0]
                G += mascara[mx - (x-1)][my - (y-1)] * self.obIma.pixeles[mx, my][1]
                B += mascara[mx - (x-1)][my - (y-1)] * self.obIma.pixeles[mx, my][2]
          newPixeles[x, y] = (R, G, B)
    else:
      for x in range(self.obIma.ancho):
        for y in range(self.obIma.alto):
          # obtenemos todos los vecinos de pixel actual
          vecindad = obtenerVecinos(x, y, self.obIma.ancho, self.obIma.alto, self.obIma.pixeles)
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

    nuevaImagen.show() # mostramos en ventana
    nuevaImagen.save('SalidaConvolucion.png') # guardamos el archivo    
    print 'LISTO'
    return nuevaImagen


  def aplicarBinarizacion(self, imagenBase, RANGO):
    print 'Aplicando binarizacion...'

    pixelesBase = imagenBase.load()
    # creamos una copia para no modificar la imagen original
    nuevaImagen = Image.new('RGB', (self.obIma.ancho, self.obIma.alto))
    newPixeles = nuevaImagen.load() 

    for x in range(self.obIma.ancho):
      for y in range(self.obIma.alto):
        # 0 = NEGRO || 255 = BLANCO
        nuevoPixel = (0, 255)[min(pixelesBase[x,y]) > RANGO] # operador ternario
        newPixeles[x, y] = (nuevoPixel, nuevoPixel, nuevoPixel)       
    
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

      w = self.obIma.ancho
      h = self.obIma.alto

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

      imagenCopia.show() # mostramos en ventana
      imagenCopia.save('SalidaObjetos.png') # guardamos el archivo
      print 'LISTO'

  def calcularDimensiones(self, objeto, imagen, mensaje=''):
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

    puntoCentro = (minX+maxX)/2, (minY+maxY)/2 # centro del objeto


    '''
    # descartamos aquellos objetos que sean muy chicos
    if minX < maxX and minY < maxY: 
      if not mensaje:
        # encerramos en un cuadrado el objeto recibido como parametro
        draw.rectangle(((minX, minY), (maxX, maxY)), outline="red")
      else:
        # escribimos en el punto centro del objeto el mensaje recibido como parametro
        puntoCentro = (minX+maxX)/2, (minY+maxY)/2 # centro del objeto
        draw.text(puntoCentro, mensaje, fill="green")
    '''

  def detectarSimilitud(self, imagenBase):
      return


def main(nombreImagen, rangoBinarizacion):
  im = Imagen(nombreImagen)
  ad = AdministradorImagen(im)

  #Mascaras de convolucion
  mascaraX, mascaraY = sobel() # cargamos la mascara, tiene que ser de 3x3

  imaGradienteXY = ad.aplicarConvolucion(mascaraX, mascaraY)

  # aplicar binarizacion
  imaBinarizada = ad.aplicarBinarizacion(imaGradienteXY, rangoBinarizacion)

  # detectar objetos
  # pixel = de que color son los objetos a buscar
  # 'blanco' = bordes || 'negro' = cosas que no sean bordes
  ad.buscarObjetos(imaBinarizada, pixel='blanco') # le mandamos la imagen 
                                                  # y el color del pixel a buscar

  # detectar circulos
  imSimilitud = ad.detectarSimilitud(imaBinarizada)

######## PARAMATROS DEL PROGRAMA #######
# [1] =(string) nombre de la imagen
# [2] = (int) rango de binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(sys.argv[1], int(sys.argv[2]))


