from PIL import Image
import json
import cv2
import numpy as np
import os

def visualize_annotations_2(json_path, source, output_dir):
    with open(json_path, 'r') as file:
        data = json.load(file)
        image_path = data["images"][source.split("/")[-1]]['words']

    img = cv2.imread(source)

    for i in image_path:
        B = image_path[i]
        A = B['points']
        pts = [(x, y) for x, y in A]
        pts = np.array(pts, dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))
        img = cv2.polylines(np.array(img), [pts], isClosed=True, color=(0, 0, 255), thickness=2)

    file_name = os.path.basename(source)
    output_path = os.path.join(output_dir, file_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cv2.imwrite(output_path, img)
    print("Finished")

# 사용 예시
json_path = '/data/ephemeral/data/medical/ufo/train.json'
source = '/data/ephemeral/data/medical/img/train/drp.en_ko.in_house.deepnatural_002754.jpg'
output_dir = '/data/ephemeral/save_bbox' 
visualize_annotations_2(json_path, source, output_dir)
