#!/usr/bin/env python
import cv2




# se crea la instancia de la captura de Video.

video = cv2.VideoCapture(0)

#Se define un ciclo.

while True:

    #Se captura el video de la webcam

    ret,im = video.read()

    #Se muestra el video  donde se pasa im que es la lectura del video de la webcam.

    cv2.imshow('Prueba de video',im)

    #Se captura la tecla de escape del teclado

    tecla = cv2.waitKey(10)

    if tecla == 27:

        #Si es la tecla escape se termina el ciclo

        break

    #Si la tecla es el espacio en blanco se captura una imagen del video.

    if tecla == ord(' '):

        cv2.imwrite('captura_img.jpg',im)