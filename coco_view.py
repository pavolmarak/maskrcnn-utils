#!/usr/bin/env python

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import copy
import itertools
import matplotlib.collections
import matplotlib.patches
from collections import defaultdict
import sys

ROOT_DIR = sys.argv[1]
ANNOT_PATH = sys.argv[2]
IMG_PATH = sys.argv[3]
CAT_NAMES = sys.argv[4:]

cat_colors = {
    '0': 'forestgreen',
    '1': 'red',
    '2': 'chocolate',
    '3': 'darkorange',
    '4': 'lawngreen',
    '5': 'aqua',
    '6': 'dodgerblue',
    '7': 'slateblue',
    '8': 'magenta',
    '9': 'sienna'

}

pylab.rcParams['figure.figsize'] = (8.0, 10.0)


def show_categories(coco_api):
    # display COCO categories and supercategories
    cats = coco_api.loadCats(coco_api.getCatIds())
    nms = [cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    nms = set([cat['supercategory'] for cat in cats])

    if None not in nms:
        print('COCO supercategories: \n{}'.format(' '.join(nms)))
    else:
        print('No supercategories found')


def get_img(coco_api, cat_names, img_path):
    # get all images containing given categories
    cat_ids = coco_api.getCatIds(catNms=cat_names)
    img_ids = coco_api.getImgIds(catIds=cat_ids)
    imgs = coco_api.loadImgs(img_ids)

    # get the desired image
    for i in imgs:
        if i['file_name'] == img_path:
            return i, cat_ids


def show_annotations(coco_api, img, cat_ids, img_path):
    # load and display instance annotations
    image = io.imread(img_path)
    plt.imshow(image)
    plt.axis('off')

    annIds = coco_api.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
    anns = coco_api.loadAnns(annIds)
    coco_api.showAnns(anns, False)
    pylab.rcParams.update({'font.size': 12})
    return anns


def show_labels(coco_api, anns):
    for item in plt.gca().collections:
        for p in item.get_paths():
            pass
    for a in anns:
        plt.annotate(str(a['category_id']), (a['bbox'][0], a['bbox'][1]), color='white')


def main():
    # initialize COCO api for instance annotations
    coco = COCO(ROOT_DIR + '/' + ANNOT_PATH)
    show_categories(coco)
    image, cat_ids = get_img(coco, CAT_NAMES, 'JPEGImages' + '/' + IMG_PATH)
    anns = show_annotations(coco, image, cat_ids, ROOT_DIR + '/' + 'JPEGImages' + '/' + IMG_PATH)
    show_labels(coco, anns)
    plt.show()


if __name__ == "__main__":
    main()
