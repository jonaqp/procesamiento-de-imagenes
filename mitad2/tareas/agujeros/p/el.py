from Tkinter import *
import Image,ImageTk
import ImageDraw
from sys import argv
from time import * 
import numpy
import matplotlib.pyplot as plt
from numpy import *
from math import floor,pi
import math
import random
class Aplicacion(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        
        self.parent = parent
        self.initUI()
   
    def initUI(self):
        self.parent.title('Ventana')
        self.pack(fill=BOTH, expand=1)
        self.o_imagen=argv[1]
        imagen = self.obtener_imagen()
        self.cargar_imagen(imagen)
        self.conv = Button(text='Agujeros', command =self.boton_agujeros).pack(side=LEFT)
        
        
    def boton_agujeros(self):
        image,horizontal,vertical = self.escala_grises()
        ima=image.save('filtrada.jpg')
        self.graficar(horizontal,vertical,image)
       # self.detectar_agujero(horizontal.vertical)
        self.cargar_imagen(image)
        return image

    def graficar(self,horizontal,vertical,image):
        plt.clf()
        fig=plt.subplot(111)
        topex=max(horizontal)
        topey=max(vertical)
        ancho,alto=image.size
        if ancho>alto:
            n=ancho
        else:
            n=alto
        if topex > topey:
            tope=topex
        else:
            tope=topey
        print 'horixontal',horizontal
        print 'vertical',vertical
        plt.ylim(-0.1 * tope,tope * 1.1)
        plt.xlim(-0.1*n,1.1*n)
        plt.title('Histograma')
       # for i in horizontal:
        x=range(1,ancho+1)
        y=range(1,alto+1)
        plt.plot(x,horizontal,'r-',linewidth=2,label='horizontal')
        plt.plot(y,vertical,'b-',linewidth=2,label='vertical')
 #plt.plot(2)
        #plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
        box = fig.get_position()
        fig.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
        fig.legend(loc = 'upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox = True, shadow = True, ncol = 1)
        plt.show()
        return
        
    def detectar_agujero(self,horizontal,vertical):
        return 
    
    def escala_grises(self):
        inicio = time()
        image = Image.open(self.o_imagen) 
        pixels = image.load()
        ancho,alto = image.size
        print 'ancho',ancho
        print 'alto',alto
        histograma_horizontal=zeros(ancho,float)
        histograma_vertical=zeros(alto,float)
        self.matriz = numpy.empty((ancho, alto))
        for i in range(ancho):
            for j in range(alto):
                (r,g,b) = image.getpixel((i,j))
                escala = (r+g+b)/3
                histograma_horizontal[i] +=escala
                histograma_vertical[j] +=escala
                pixels[i,j] = (escala,escala,escala)
                self.matriz[i,j] = int(escala)
        fin = time()
        tiempo_t = fin - inicio
       # print "Tiempo que tardo en ejecutarse escala de grises = "+str(tiempo_t)+" segundos"
        df = image.save('escala.png')
        return image,histograma_horizontal,histograma_vertical

    
   
    
    def obtener_imagen(self):
        imagen = Image.open(self.o_imagen)
        imagen = imagen.convert('RGB')
        return imagen


    def cargar_imagen(self,imagen):
        img = ImageTk.PhotoImage(imagen) 
        label = Label(self, image=img)
        label.imagen = img
        label.place(x=10, y=10)

def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()
    
main()
