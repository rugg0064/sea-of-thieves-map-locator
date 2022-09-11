
import os
from PIL import Image
import imagehash
import numbers
import skimage
import numpy as np
from skimage import exposure

imagePath = './mapSamples/image1.png'
outputPath = './contrastedSamples/image1.png'
image = Image.open(imagePath)


na = np.array(image)

percentiles = np.percentile(na, (0.00005, 99.9995))
image_minmax_scaled = exposure.rescale_intensity(na, in_range=tuple(percentiles))

outputImage = Image.fromarray(image_minmax_scaled)

outputImage.save(outputPath)