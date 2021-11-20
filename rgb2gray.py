from PIL import Image
import sys

img = Image.open(sys.argv[1]).convert('L')
img.save('gray_'+sys.argv[1], quality=95)
