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
    crop_counter = 0
    for img in data['images']:
        img_crops = {}
        curr_img = Image.open(img['file_name'])
        img_crops['id'] = img['id']
        img_crops['path'] = img['file_name']
        img_crops['crops'] = []

        for w in range(0, curr_img.width, block_w):
            for h in range(0, curr_img.height, block_h):
                img_crops['crops'].append({
                    'id': crop_counter,
                    'img_data': curr_img.crop([w, h, w + block_w, h + block_h]),
                    'left': w,
                    'top': h,
                    'width': block_w,
                    'height': block_h,
                    'crop_name': destination_folder + '/' + img_crops['path'].split('/')[-1] + '_col' + str(
                        w) + '_row' + str(h) + '.jpg'
                })
                img_crops['crops'][-1]['img_data'].save(img_crops['crops'][-1]['crop_name'])
                crop_counter = crop_counter + 1

        images.append(img_crops)
    return images


# checks if an image crop contains annotations
def has_annotations(data_json, crop):
    for ann in data_json['annotations']:
        if ann['image_id'] == crop['id']:
            return True
    return False


def update_images_json(data_json, images):
    data_json['images'].clear()
    for img in images:
        for crop in img['crops']:
            if has_annotations(data_json, crop) is False:
                os.remove(crop['crop_name'])
                continue

            data_json['images'].append(
                {
                    'license': 0,
                    'url': None,
                    'file_name': crop['crop_name'],
                    'height': block_h,
                    'width': block_w,
                    'date_captured': None,
                    'id': crop['id']
                }
            )
    return data_json


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


def update_annotations_json(data_json, images):
    annotations = []
    anns_in_crop = []
    for img in images:
        for crop in img['crops']:
            anns_in_crop = get_annotations_in_crop(data_json, crop, img['id'])
            for ann in range(len(anns_in_crop)):
                # transform image_id
                anns_in_crop[ann]['image_id'] = crop['id']
                # transform segmentation
                for polygon in range(len(anns_in_crop[ann]['segmentation'])):
                    for i in range(len(anns_in_crop[ann]['segmentation'][polygon])):
                        if i % 2 == 0:
                            anns_in_crop[ann]['segmentation'][polygon][i] = anns_in_crop[ann]['segmentation'][polygon][
                                                                                i] - crop['left']
                        else:
                            anns_in_crop[ann]['segmentation'][polygon][i] = anns_in_crop[ann]['segmentation'][polygon][
                                                                                i] - crop['top']
                # transform bbox
                anns_in_crop[ann]['bbox'][0] = anns_in_crop[ann]['bbox'][0] - crop['left']
                anns_in_crop[ann]['bbox'][1] = anns_in_crop[ann]['bbox'][1] - crop['top']

            annotations = annotations + anns_in_crop
    data_json['annotations'] = annotations
    return data_json


with open(ann_file) as json_file:
    data_json = json.load(json_file)

    # make image crops
    images = make_crops(data_json, destination_folder, block_w, block_h)

    # update annotations in JSON
    data_json = update_annotations_json(data_json, images)

    # update images in JSON
    data_json = update_images_json(data_json, images)

    with open('annotations-new.json', 'w') as outfile:
        json.dump(data_json, outfile)
