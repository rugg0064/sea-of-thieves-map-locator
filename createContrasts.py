import os
from PIL import Image
import numbers
from normalizing import *

inPath = './originalImages/'
outPath = './normalizedImages/'

def getContrast(image):
    returnImage = image.copy()
    for i in range(returnImage.size[0]): # for every pixel:
        for j in range(returnImage.size[1]):
            pixel = returnImage.getpixel((i, j))
            isMostlyBlue = (pixel[2] > pixel[1] and pixel[2] > pixel[0])
            isTransparent = pixel[3] < 255
            blueToGreen = abs(pixel[1] - pixel[2])
            bluetoRed = abs(pixel[0] - pixel[2])
            isGray = blueToGreen < 50 and bluetoRed < 50
            if((isMostlyBlue and not isGray) or isTransparent):
                returnImage.putpixel((i, j), (0,0,0))
            else:
                returnImage.putpixel((i, j), (0xFF, 0xFF, 0xFF))
    return returnImage

for root, dirs, files in os.walk(inPath):
    for file in files:
        image = Image.open(inPath + file)
        image = getContrast(image)
        image = getBoundedImage(image)
        image = proportionalResize(image)
        image = placeOntoCentered(image)
        image.save(f'{outPath}{file}')