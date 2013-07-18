import Image
import sys

import GIF
import Directory

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def difference(ima, ima2, UMBRAL=50):
    ''' 
        You create a new image and the values of its pixels is the difference
        of tha images selected.
    '''

    w = ima.size[0] # take a image of the list and get its dimensions
    h = ima.size[1]

    pix = ima.load() # load pixels
    pix2 = ima2.load() # load pixels

    # create a new image that will be the difference of both pixeles. 
    # To see the moviment.
    newImage = Image.new('RGB', (w,h))
    newPix = newImage.load()

    soloIma = Image.new('RGB', (w,h))
    soloPix = soloIma.load()
    
    for y in range(h):
        for x in range(w):
            if(pix2[x,y][0] - pix[x,y][0]) > UMBRAL:
                newPix[x,y] = RED # there was movement
                soloPix[x,y] = RED 
            else:
                newPix[x,y] = pix2[x,y] # stays the same
                soloPix[x,y] = WHITE 
    return(newImage, soloIma)


def detectMotion(images):
    print 'Looking for differences in pixeles...'
 
    motionPixels = list()
    pixeles = list()
    for i in range(len(images)-1):
        (newImage, soloIma) = difference(images[i], images[i+1])
        motionPixels.append(newImage)
        pixeles.append(soloIma)
    print 'READY'
    return(motionPixels, pixeles)


def saveImage(images):
    number = 0
    for i in images:
        i.save(str(number+1)+'.png') # save the file   
        number += 1 


def main(nombreGif):    
    (folder1, folder2) = Directory.createDirectory()

    # read the gif
    images = GIF.readGif(nombreGif)

    # play with scanned images
    (motionPixels, pixeles) = detectMotion(images)

    # save files
    Directory.movedir(folder1)
    saveImage(motionPixels)
    Directory.creatGif()
    Directory.backDirectory()
    
    Directory.movedir(folder2)
    saveImage(pixeles)
    Directory.creatGif()
    Directory.backDirectory()



##### Parametros del programa ####
#[1] = .gif name
##################################
main(sys.argv[1])


