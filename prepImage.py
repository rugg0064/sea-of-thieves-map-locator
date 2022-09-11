from PIL import Image
import sys
import numpy
import skimage

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

inputPath = sys.argv[1]
outputPath = sys.argv[2]

img = Image.open(inputPath)
img = img.resize((295,295), 0)

threshold = 255
bestImage = None
while(threshold >= 0):
    newImage = grayscaleAverageContrast(img, threshold)
    edgeBlack = isEdgeBlack(newImage)
    print(f"Trying {threshold}: {edgeBlack}")
    if(edgeBlack):
        bestImage = newImage
    else:
        break
    threshold = threshold - 1
    
if bestImage is not None:
    #bestImage.save(outputPath)
    bestImage.save('./asd1.png')
    na = numpy.array(bestImage)
    for i in range(5):
        na = skimage.morphology.dilation(na, skimage.morphology.ball(4))
        na = skimage.morphology.erosion(na, skimage.morphology.ball(4))
    bestImage = Image.fromarray(na)
    bestImage.save('./asd2.png')