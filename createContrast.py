
import os
from PIL import Image
import imagehash
import numbers

path = './originalImages/'
newPath = './newContrasts/'
for root, dirs, files in os.walk(path):
    for file in files:
        imagePath = path + file
        print(imagePath)
        image = Image.open(imagePath)
        pixels = image.load()
        for i in range(image.size[0]): # for every pixel:
            for j in range(image.size[1]):
                pixel = image.getpixel((i, j))
                isMostlyBlue = (pixel[2] > pixel[1] and pixel[2] > pixel[0])
                isTransparent = pixel[3] < 255
                blueToGreen = abs(pixel[1] - pixel[2])
                bluetoRed = abs(pixel[0] - pixel[2])
                isGray = blueToGreen < 50 and bluetoRed < 50

                if((isMostlyBlue and not isGray) or isTransparent):
                    image.putpixel((i, j), (0,0,0))
                else:
                    image.putpixel((i, j), (0xFF, 0xFF, 0xFF))
        image.save(newPath + file)
        