import json, sys
from shapely.geometry import Polygon


ann_path = sys.argv[1]
new_width = int(sys.argv[2]) 
new_height = int(sys.argv[3]) 

with open(ann_path) as json_file:
    data = json.load(json_file)

    # zmena rozmerov obrazku
    for img in data['images']:
        img['width'] = new_width
        img['height'] = new_height
        print(img['width'])
        print(img['height'])

    # zmena anotacii (suradnice, bbox, area)
    for ann in data['annotations']:
        
        # suradnice
        points = []
        for seg in ann['segmentation']:
            counter = 0
            for i in range(len(seg)):
                if counter % 2 == 0:
                    seg[i] = seg[i] * new_width / 4160
                else:
                    seg[i] = seg[i] * new_height / 6240
                    points.append((seg[i-1], seg[i]))
                counter = counter + 1
        polygon = Polygon(points)
       
        # bbox
        new_bbox = [polygon.bounds[0], polygon.bounds[3]-(polygon.bounds[3] - polygon.bounds[1]), polygon.bounds[2] - polygon.bounds[0], polygon.bounds[3] - polygon.bounds[1]]
        for i in range(len(ann['bbox'])):
            ann['bbox'][i] = new_bbox[i]
            print(ann['bbox'][i])

        
        # area
        ann['area'] = polygon.area
        print(ann['area'])

    with open('annotations-new.json', 'w') as outfile:
        json.dump(data, outfile)
