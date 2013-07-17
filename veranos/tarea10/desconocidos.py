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
    print self.imagen.size, self.imagen.mode

class AdministradorImagen(object):
  def __init__(self, imagen):
    self.obIma = imagen

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

  def dibujarCirculos(self, imagenBase, cordenadas, radio):
    umbral = 2
    
    pixlesBase = imagenBase.load()
    draw = ImageDraw.Draw(self.obIma.imagen)

    for x, y in cordenadas:
      v1 = v2 = v3 = v4 = False

      for k in range(-umbral, umbral):
        curr_radio = radio+k

        if (x+curr_radio)<self.obIma.ancho and (x+curr_radio)>0 and (x-curr_radio)<self.obIma.ancho and (x-curr_radio)>0:

          if pixlesBase[x+curr_radio, y] != (0, 0, 0):
            v1 = True

          if pixlesBase[x-curr_radio, y] != (0, 0, 0):
            v2 = True

        if (y+curr_radio)<self.obIma.alto and (y+curr_radio)>0 and (y-curr_radio)<self.obIma.alto and  (y-curr_radio)>0:
          if pixlesBase[x, y+curr_radio] != (0, 0, 0):
            v3 = True

          if pixlesBase[x, y-curr_radio] != (0, 0, 0):
            v4 = True

          if v1 and v2 and v3 and v4:
            draw.ellipse((x-radio, y-radio, x+radio, y+radio), outline ='red')
            print '    * circulo con radio', radio    
            break
    self.obIma.imagen.save('SalidaCirculos.png')


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

    ancho = self.obIma.ancho
    alto = self.obIma.alto

    votos = self.zeros(ancho, alto)

    for x in range(ancho):
      for y in range(alto):
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
            if centroX>=0 and centroX<ancho and centroY>=0 and centroY<alto:
              votos[centroX][centroY] += 1

    votos = self.votacionPixeles(votos, (ancho, alto))
    
    maximo = 0
    suma = 0.0
    for x in range(ancho):
      for y in range(alto):
        v = votos[x][y]
        suma += v
        if v>maximo:
          maximo = v

    promedio = suma / (ancho*alto)
    umbral = (maximo+promedio) / 2.0

    cordenadas = []
    for x in range(ancho):
      for y in range(alto):
        v = votos[x][y]
        if v>umbral:
          cordenadas.append((x, y))
    return cordenadas


  def detectarCirculos(self, imagenBase, imaGradienteX, imaGradienteY, salto=3):
    print 'Detectando circulos radio desconocido...'
    radioMinimo = 6
    radioMaximo = int((self.obIma.ancho**2 + self.obIma.ancho**2)**0.5 /3)

    print '    Radio minimo:', radioMinimo
    print '    Radio maximo:', radioMaximo
    print '    Con salto de:', salto, 'pixeles'

    # hacemos el recorrido por todos los radios posibles
    for radio in range(radioMinimo, radioMaximo, salto):
      cordenadas = self.buscarCentros(radio, imaGradienteX, imaGradienteY)
      self.dibujarCirculos(imagenBase, cordenadas, radio)

    print 'LISTO'


def main(nombreImagen, rangoBinarizacion):
  im = Imagen(nombreImagen)
  ad = AdministradorImagen(im)

  #Mascaras de convolucion
  mascaraX, mascaraY = sobel() # cargamos la mascara, tiene que ser de 3x3
  ambos = [[0, 2, 2], [-2, 0, 2], [-2, -2, 0]]

  # aplicar convolucion para gx
  imaGradienteX = ad.aplicarConvolucion(mascaraX)
  # aplicar convolucion para gy
  imaGradienteY = ad.aplicarConvolucion(mascaraY) 
  # aplicar convolucion para gx y gy
  #imaGradienteXY = ad.aplicarConvolucion(ambos)
  imaGradienteXY = ad.aplicarConvolucion(mascaraX, mascaraY)


  # aplicar binarizacion
  imaBinarizada = ad.aplicarBinarizacion(imaGradienteXY, rangoBinarizacion)

  # detectar circulos
  ad.detectarCirculos(imaBinarizada, imaGradienteX, imaGradienteY)

######## PARAMATROS DEL PROGRAMA #######
# [1] =(string) nombre de la imagen
# [2] = (int) rango de binarizacion - numero entre 0-255(mientras mas bajo bordes mas gruesos)
########################################
main(sys.argv[1], int(sys.argv[2]))


