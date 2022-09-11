from PIL import Image
import numpy
import skimage
import os
import imagehash
import sys
from normalizing import *

def grayscaleAverageContrast(original, threshold):
    image = original.copy()
    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            pixel = image.getpixel((i, j))
            average = (pixel[0] + pixel[1] + pixel[2]) / 3
            if(average < threshold):
                image.putpixel((i, j), (0,0,0))
            else:
                image.putpixel((i, j), (255, 255, 255))
    return image

def isEdgeBlack(image):
    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            iIsEdge = (i == 0) or (i == image.size[0] - 1)
            jIsEdge = (j == 0) or (j == image.size[1] - 1)
            if(iIsEdge or jIsEdge):
                pixel = image.getpixel((i, j))
                if(not (pixel == (0,0,0) or pixel == (0,0,0,255))):
                    return False
    return True

def holeFill(image, count, size):
    na = numpy.array(image)
    for i in range(count):
        na = skimage.morphology.dilation(na, skimage.morphology.ball(size))
        na = skimage.morphology.erosion(na, skimage.morphology.ball(size))
    returnImage = Image.fromarray(na)
    return returnImage

def prepImage(image):
    img = image
    print('contrasting image')
    bestImage = None
    top = 256
    bottom = 0
    while(top != bottom):
        midpoint = (top + bottom) // 2
        newImage = grayscaleAverageContrast(img, midpoint)
        edgeBlack = isEdgeBlack(newImage)
        if(edgeBlack):
            top = midpoint
            bestImage = newImage
        else:
            if(bottom == midpoint):
                bottom = midpoint + 1
            else:
                bottom = midpoint
    print(f'Settled on contrast {bottom}')
    returnImage = grayscaleAverageContrast(img, min(255, midpoint + 5))
    #returnImage = returnImage.convert('RGB')
    skimageImage = numpy.array(returnImage)
    for i in range(3):
        skimageImage = skimage.morphology.closing(skimageImage, footprint = skimage.morphology.ball(4))
    returnImage = Image.fromarray(skimageImage)
    return returnImage

def alternateComparison(img1, img2, printer):
    wrongCount = 0
    for i in range(img1.size[0]): # for every pixel:
        for j in range(img1.size[1]):
            pixel1 = img1.getpixel((i, j))
            pixel2 = img2.getpixel((i, j))
            if(pixel1 != pixel2):
                wrongCount = wrongCount + 1
    return wrongCount

def scriptMain(imagePath):
    img = Image.open(imagePath)
    ratio = img.size[0] / img.size[1]
    img = img.resize((128,int(128 * ratio)))
    img = prepImage(img)
    img = normalizeTo256(img)
    img = grayscaleAverageContrast(img, 128)
    if(img is None):
        print("Couldn't prep image.")
        exit()
    hash = imagehash.average_hash(img)
    min = 9999999
    minName = ''
    path = './normalizedImages/'
    for root, dirs, files in os.walk(path):
        for file in files:
            imagePath = path + file
            otherImg = Image.open(imagePath)
            otherImg = otherImg.resize((128,128))
            otherHash = imagehash.average_hash(otherImg)
            score = hash - otherHash
            #score = alternateComparison(img, otherImg, 'lonely' in file)
            if(score < min):
                min = score
                minName = imagePath
            #print(imagePath, score)
    print('best: ' + minName)

if __name__ == '__main__':
    scriptMain(sys.argv[1])