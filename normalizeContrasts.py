import os
from PIL import Image
import imagehash
import numbers

inPath = './newContrasts/'
outPath = './normalizedImages/'

def getBoundedImage(image):
    x1, x2, y1, y2 = 255, 0, 255, 0
    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            pixel = image.getpixel((i, j))
            if(pixel == (255, 255, 255) or pixel == (255, 255, 255, 255)):
                x1 = min(i, x1)
                x2 = max(i, x2)
                y1 = min(j, y1)
                y2 = max(j, y2)
    newImage = Image.new('RGBA', (x2 - x1 + 1, y2 - y1 + 1))
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            if(image.getpixel((i, j)) == (255, 255, 255, 255) ):
                newImage.putpixel( (i - x1, j - y1), (255, 255, 255 ,255) )
            else:
                newImage.putpixel( (i - x1, j - y1), (0, 0, 0, 255) )
    return newImage

#Turns into image with the longest edge of length 256
def proportionalResize(image):
    width = image.size[0]
    height = image.size[1]
    ratio = width / height
    newSize = (0, 0)
    if(ratio > 1):
        newSize = (256, int(256 / ratio))
    else:
        newSize = (int(256 * ratio), 256)
    return image.resize(newSize)

def placeOntoCentered(image):
    newImage = Image.new('RGBA', (256, 256))
    for i in range(newImage.size[0]): # for every pixel:
        for j in range(newImage.size[1]):
            newImage.putpixel((i, j), (0, 0, 0, 255))
    width = image.size[0]
    height = image.size[1]
    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            x = 128 - (width // 2) + i
            y = 128 - (height // 2) + j
            if(x >= 256 or y >= 256):
                continue
            pixel = image.getpixel((i, j))
            newImage.putpixel((x, y), pixel)
    return newImage
    

for root, dirs, files in os.walk(inPath):
    for file in files:
        image = Image.open(inPath + file)
        image = getBoundedImage(image)
        image = proportionalResize(image)
        image = placeOntoCentered(image)
        image.save(f'{outPath}{file}')
