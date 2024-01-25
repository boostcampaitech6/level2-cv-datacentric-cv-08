from PIL import Image
import json
import cv2
import numpy as np
import os

def visualize_annotations_2(json_path, source, output_dir):
    """
    Image 에 bbox를 Opencv 사용하여 가시화 후 저장
    

    Args:
        json_path (_type_): Annotation json file path
        source (_type_): Image file path
        output_dir (_type_): bbox visualization image storage dir path
    """    
    tag = ['masked', 'maintable', 'excluded-region', 'stamp']
    select = True
    with open(json_path, 'r') as file:
        data = json.load(file)
        image_path = data["images"][source.split("/")[-1]]['words']

    img = cv2.imread(source)

    for i in image_path:
        B = image_path[i]
        select = True
        for j in B['tags']:
            if j in tag:
                select = False
                continue
        if select:
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


json_path = '/data/ephemeral/data/medical/ufo/train.json'
source = '/data/ephemeral/data/medical/img/train/drp.en_ko.in_house.deepnatural_002754.jpg'
output_dir = '/data/ephemeral/save_bbox' 
visualize_annotations_2(json_path, source, output_dir)
