import sys
import os
import json
from shapely.geometry import Polygon
from PIL import Image

destination_folder = sys.argv[1]
imgs = sys.argv[2:]
block_w = 128
block_h = 128

if os.listdir(destination_folder):
    print("ERROR: Directory is not empty")
    sys.exit()


def make_crops(imgs, destination_folder, block_w, block_h):
    for img in imgs: 
        curr_img = Image.open(img)
        for w in range(0, curr_img.width, block_w):
            for h in range(0, curr_img.height, block_h):
                cimg = curr_img.crop([w, h, w + block_w, h + block_h])
                crop_name = destination_folder + '/' + img.split('/')[-1] + '_col' + str(w) + '_row' + str(h) + '.jpg'
                cimg.save(crop_name)



make_crops(imgs, destination_folder, block_w, block_h)

