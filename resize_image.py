#!/usr/bin/python
from PIL import Image
import os, sys

path = "./"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if item.endswith('JPG') is True:
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((667,1000), Image.ANTIALIAS)
            imResize.save(f + '_resized.jpg', 'JPEG', quality=100)

resize()
