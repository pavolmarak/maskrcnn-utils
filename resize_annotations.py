import json
from shapely.geometry import Polygon

with open('annotations.json') as json_file:
    data = json.load(json_file)

    # zmena rozmerov obrazku
    for img in data['images']:
        img['width'] = 667
        img['height'] = 1000
        print(img['width'])  # 667
        print(img['height'])  # 1000

    # zmena anotacii (suradnice, bbox, area)
    for ann in data['annotations']:
        
        # suradnice
        points = []
        for seg in ann['segmentation']:
            counter = 0
            for i in range(len(seg)):
                if counter % 2 == 0:
                    seg[i] = seg[i] * 667 / 4160
                else:
                    seg[i] = seg[i] * 1000 / 6240
                    points.append((seg[i-1], seg[i]))
                counter = counter + 1
        polygon = Polygon(points)
       
        # bbox
        new_bbox = [polygon.bounds[0], polygon.bounds[3]-(polygon.bounds[3] - polygon.bounds[1), polygon.bounds[2] - polygon.bounds[0], polygon.bounds[3] - polygon.bounds[1]]
        for i in range(len(ann['bbox'])):
            ann['bbox'][i] = new_bbox[i]
            print(ann['bbox'][i])

        
        # area
        ann['area'] = polygon.area
        print(ann['area'])

    with open('annotations-new.json', 'w') as outfile:
        json.dump(data, outfile)
