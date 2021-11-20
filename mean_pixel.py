from PIL import Image, ImageStat
import sys

# computes a mean pixel in grayscale image

img = Image.open(sys.argv[1])

if img.mode == 'RGB':
    print('Error: RGB image instead of grayscale.')
else:
    stat = ImageStat.Stat(img)
    print('Mean ' + str(stat.mean))
