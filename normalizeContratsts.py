import os
from PIL import Image
import imagehash
import numbers
from normalizing import *

inPath = './newContrasts/'
outPath = './normalizedImages/'

for root, dirs, files in os.walk(inPath):
    for file in files:
        image = Image.open(inPath + file)
        image = getBoundedImage(image)
        image = proportionalResize(image)
        image = placeOntoCentered(image)
        image.save(f'{outPath}{file}')
