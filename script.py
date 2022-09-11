import os
from PIL import Image
import imagehash
import sys

ogPath = sys.argv[1]
#ogPath = './contrastedSamples/image5.png'
img = Image.open(ogPath)
img = img.resize((295,295), 0)
hash = imagehash.whash(img)

min = 9999999
minName = ''
path = './newContrasts/'
for root, dirs, files in os.walk(path):
    for file in files:
        imagePath = path + file
        otherImg = Image.open(imagePath)
        otherHash = imagehash.whash(otherImg)
        score = hash - otherHash
        if(score < min):
            min = score
            minName = imagePath
        print(imagePath, score)
print()
print('best: ' + minName)