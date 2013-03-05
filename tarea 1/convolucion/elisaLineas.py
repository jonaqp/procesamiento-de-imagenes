from math import pi, atan, floor, fabs, sqrt, sin, cos, ceil
from sys import argv

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
        print frecuencia
    return incluidos

def valorDeVecinos(imagen, x, y, w, h):
    resultado = list()
    for deltax in [-1, 0, 1]:
        posx = x + deltax
        if posx >= 0 and posx < w:
            for deltay in [-1, 0, 1]:
                posy = y + deltay
                if posy >= 0 and posy < h:
                    resultado.append(imagen[posy][posx])
    return resultado    

def normalize(d):
    h = len(d)
    w = len(d[0])
    minimo = min(min(d))
    maximo = max(max(d))
    div = maximo - minimo
    for y in xrange(h):
        for x in xrange(w):
            d[y][x] = (d[y][x] - minimo) / div
    return d

def euclidean(dx, dy):
    h = len(dx)
    w = len(dx[0])
    m = list()
    for y in xrange(h):
        c = list()
        for x in xrange(w):
            c.append(sqrt(dx[y][x]**2 + dy[y][x]**2))
        m.append(c)
    return m

def convolucion(imagen, mascara):
    resultado = list()
    h = len(imagen)
    w = len(imagen[0])
    for y in xrange(h):
        fila = list()
        for x in xrange(w):
            valor = 0.0
            k = len(mascara[0])
            for i in xrange(k):
                dx = i - (k / 2)
                l = len(mascara)
                for j in xrange(l):
                    dy = j - (l / 2)
                    ix = x + dx
                    iy = y + dy
                    if ix >= 0 and ix < w and iy >= 0 and iy < h:
                        valor += imagen[iy][ix] * mascara[j][i]
            fila.append(valor)
        resultado.append(fila)
    return resultado

try:
    incluir = float(argv[1])
except:
    try:
        incluir = float(fabs(int(raw_input('Cuantos considerar: '))))
    except:
        incluir = 0.1

imagen = list()
entrada = open('numerico.txt', 'r')
for linea in entrada.readlines():
    linea = linea.strip()
    if len(linea) > 0:
        fila = list()
        for columna in linea:
            fila.append(int(columna))
        imagen.append(fila)
entrada.close()

sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

CERO = 0.00001

gx = convolucion(imagen, sobelx)
gy = convolucion(imagen, sobely)
m = normalize(euclidean(gx, gy))

resultado = list()
w = len(imagen[0])
h = len(imagen)

for y in xrange(h):
    datos = list()
    for x in xrange(w):
        hor = gx[y][x]
        ver = gy[y][x]
        magnitud = m[y][x]
        if fabs(hor) > CERO:
            angulo = atan(ver / hor) # RELEVANTE
        else:
            if fabs(hor) + fabs(ver) < CERO:
                angulo = None # aqui no hay nada en ninguna direccion
            elif fabs(ver - hor) < CERO: # casi iguales
                angulo = atan(1.0)
            elif hor * ver > 0.0: # mismo signo
                angulo = pi 
            else: # negativo -> -pi
                angulo = 0.0
        # eje vertical volteado y origen al centro
        if angulo is not None:
            # asegurar que este entre cero y pi (0 y 180)
            while angulo < CERO:
                angulo += pi
            while angulo > pi:
                angulo -= pi
            rho = (x - w/2) * cos(angulo) + (h/2 - y) * sin(angulo) # RELEVANTE
            # hay que discretizar - RELEVANTE
            datos.append((magnitud, '%.0f' % (int(180 * (angulo / pi)) / 18), '%.0f' % rho))
        else:
            datos.append((None, None, None))
    resultado.append(datos)

comb = dict()
# recorre todo los resultados arrojados por los pixeles y suma los frecuentes
for y in xrange(h):
    for x in xrange(w):
        # no incluir bordes (meten ruido)
        if x > 0 and y > 0 and x < w - 1 and y < h - 1: 
            (magnitud, angulo, rho) = resultado[y][x]
            if magnitud is not None:
                combinacion = (angulo, rho)
                if combinacion in comb:
                    comb[combinacion] += 1
                else:
                    comb[combinacion] = 1
print comb
raw_input()

frec = frecuentes(comb, int(ceil(len(comb) * incluir))) # RELEVANTE

print 'Son %d combinaciones presentes' % len(comb)
print 'Usamos a', len(frec), 'de ellas'

procesado = list()
falsoPositivo = 0
falsoNegativo = 0
correctoPositivo = 0
correctoNegativo = 0
for y in xrange(h):
    renglon = list()
    for x in xrange(w):
        (mag, ang, rho) = resultado[y][x]
        vecindad = valorDeVecinos(imagen, x, y, w, h)
        deberia = (imagen[y][x] == 9)
        if (ang, rho) in frec: # RELEVANTE
            if deberia:
                renglon.append('X') # correcto
                correctoPositivo += 1
            else:
                renglon.append('?') # imaginario encontrado
                falsoPositivo += 1
        else:
            if deberia:
                renglon.append('!') # no linea pero deberia
                falsoNegativo += 1
#                print '#', y, x, mag, ang, rho
            else:
                renglon.append('-') # no linea ni debe
                correctoNegativo += 1
        imagen[y][x] = ('%d' % imagen[y][x])
    procesado.append(renglon)
numero = 0
for linea in imagen:
    print '%2d' % numero, ''.join(linea), ''.join(procesado.pop(0))
    numero += 1
incorrecto = falsoPositivo + falsoNegativo
print False, falsoPositivo, '+', falsoNegativo, '=', incorrecto
correcto = correctoPositivo + correctoNegativo
print True, correctoPositivo, '+', correctoNegativo, '=', correcto
print '%.0f por ciento correcto' % ((correcto * 100.0) / (correcto + incorrecto))