import sys
import os
import json
from shapely.geometry import Polygon
from PIL import Image

ann_file = sys.argv[1]
destination_folder = sys.argv[2]

if os.listdir(destination_folder):
    print("ERROR: Directory is not empty")
    sys.exit()

with open(ann_file) as json_file:
    data = json.load(json_file)
    imgs = {}
    for img in data['images']:
        imgs[img['id']] = Image.open(img['file_name'])
    data['images'].clear()
    cnts = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0
    }
    ann_id = 0
    for ann in data['annotations']:
        img = imgs[ann['image_id']]
        img_cropped = img.crop((
            ann['bbox'][0],
            ann['bbox'][1],
            ann['bbox'][0] + ann['bbox'][2],
            ann['bbox'][1] + ann['bbox'][3]))
        img_cropped.save(
            destination_folder + '/' + str(ann['category_id']) + '_' + str(cnts[ann['category_id']]) + '.jpg',
            quality=95)
        width, height = img_cropped.size
        data['images'].append({
            'license': 0,
            'url': None,
            'file_name': 'JPEGImages/' + str(ann['category_id']) + '_' + str(cnts[ann['category_id']]) + '.jpg',
            'height': height,
            'width': width,
            'date_captured': None,
            'id': ann_id
        })
        ann['image_id'] = ann_id
        for seg in ann['segmentation']:
            counter = 0
            for i in range(len(seg)):
                if counter % 2 == 0:  # x
                    seg[i] = seg[i] - ann['bbox'][0]
                else:  # y
                    seg[i] = seg[i] - ann['bbox'][1]
                counter = counter + 1

        ann['bbox'] = [0, 0, width, height]

        cnts[ann['category_id']] = cnts[ann['category_id']] + 1
        ann_id = ann_id + 1

    with open('annotations-new.json', 'w') as outfile:
        json.dump(data, outfile)
    print(cnts)
