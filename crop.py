import sys
import os
import json
from shapely.geometry import Polygon
from PIL import Image

ann_file = sys.argv[1]
destination_folder = sys.argv[2]
block_w = 128
block_h = 128

if os.listdir(destination_folder):
    print("ERROR: Directory is not empty")
    sys.exit()


def make_crops(data, destination_folder, block_w, block_h):
    images = []
    for img in data['images']:
        img_crops = {}
        curr_img = Image.open(img['file_name'])
        img_crops['id'] = img['id']
        img_crops['path'] = img['file_name']
        img_crops['crops'] = []

        for w in range(0, curr_img.width, block_w):
            for h in range(0, curr_img.height, block_h):
                img_crops['crops'].append({
                    'img_data': curr_img.crop([w, h, w + block_w, h + block_h]),
                    'left': w,
                    'top': h,
                    'width': block_w,
                    'height': block_h,
                    'crop_name': destination_folder + '/' + img_crops['path'].split('/')[-1] + '_col' + str(w) + '_row' + str(h) + '.jpg'
                })
                img_crops['crops'][-1]['img_data'].save(img_crops['crops'][-1]['crop_name'])

        images.append(img_crops)
    return images


def set_images_field(data, images):
    data['images'].clear()
    cnt = 0
    for img in images:
        for crop in img['crops']:
            data['images'].append(
                {
                    'license': 0,
                    'url': None,
                    'file_name': crop['crop_name'],
                    'height': block_h,
                    'width': block_w,
                    'date_captured': None,
                    'id': cnt
                }
            )
            cnt = cnt + 1
    return data


def is_bbox_in_crop(bbox, crop):
    if bbox[0] >= crop['left'] and \
            bbox[0] + bbox[2] <= crop['left'] + crop['width'] and \
            bbox[1] >= crop['top'] and \
            bbox[1] + bbox[3] <= crop['top'] + crop['height']:
        return True
    return False


def get_annotations_in_crop(data, crop, orig_image_id):
    anns = []
    # get all anns for orig_image_id
    for ann in data['annotations']:
        if ann['image_id'] == orig_image_id:
            # that belong to the crop
            if is_bbox_in_crop(ann['bbox'], crop) is True:
                anns.append(ann)
    return anns


def transform_annotations(data, images):
    annotations = []
    anns_in_crop = []
    crop_counter = 0
    for img in images:
        for crop in img['crops']:
            anns_in_crop = get_annotations_in_crop(data, crop, img['id'])
            for ann in range(len(anns_in_crop)):
                # transform image_id
                anns_in_crop[ann]['image_id'] = crop_counter
                # transform segmentation
                for polygon in range(len(anns_in_crop[ann]['segmentation'])):
                    for i in range(len(anns_in_crop[ann]['segmentation'][polygon])):
                        if i % 2 == 0:
                            anns_in_crop[ann]['segmentation'][polygon][i] = anns_in_crop[ann]['segmentation'][polygon][i] - crop['left']
                        else:
                            anns_in_crop[ann]['segmentation'][polygon][i] = anns_in_crop[ann]['segmentation'][polygon][i] - crop['top']
                # transform bbox
                anns_in_crop[ann]['bbox'][0] = anns_in_crop[ann]['bbox'][0] - crop['left']
                anns_in_crop[ann]['bbox'][1] = anns_in_crop[ann]['bbox'][1] - crop['top']

            annotations = annotations + anns_in_crop
            crop_counter = crop_counter + 1
    data['annotations'] = annotations
    return data


with open(ann_file) as json_file:
    data = json.load(json_file)

    # make crops
    images = make_crops(data, destination_folder, block_w, block_h)

    # transform annotations
    data = transform_annotations(data, images)

    # set images field
    data = set_images_field(data, images)

    with open('annotations-new.json', 'w') as outfile:
        json.dump(data, outfile)
