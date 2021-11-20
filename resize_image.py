#!/usr/bin/python
from PIL import Image
import os, sys

img_path = sys.argv[1]
new_width = int(sys.argv[2])
new_height = int(sys.argv[3])

def resize(img_path):
        if img_path.endswith('jpg') is True:
            im = Image.open(img_path)
            f, e = os.path.splitext(img_path)
            imResize = im.resize((new_width,new_height), Image.ANTIALIAS)
            imResize.save(f + '_resized.jpg', 'JPEG', quality=95)

resize(img_path)
