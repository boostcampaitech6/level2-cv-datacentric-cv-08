from PIL import Image
import json
import cv2
import numpy as np
import os
import csv

def visualize_annotations_json(json_path, source, output_dir):
    """
    json 형태의 annotation file 을 읽고 
    Image 에 bbox를 Opencv 사용하여 가시화 후 저장

    Args:
        json_path (_type_): Annotation json file path
        source (_type_): Image file path
        output_dir (_type_): bbox visualization image storage dir path
    """    
    # 예외 tag 정리
    tag = ['masked', 'maintable', 'excluded-region', 'stamp']
    select = True

    with open(json_path, 'r') as file:
        data = json.load(file)
        image_path = data["images"][source.split("/")[-1]]['words']

    img = cv2.imread(source)

    for i in image_path:
        B = image_path[i]
        select = True
        
        # 예외 tag가 포함되어 있다면 건너뛰기
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

def visualize_annotations_csv(csv_path, source, output_dir):
    """
    csv 형태의 annotation file 을 읽고 
    Image 에 bbox를 Opencv 사용하여 가시화 후 저장

    Args:
        csv_path (_type_): Annotation csv file path
        source (_type_): Image file path
        output_dir (_type_): bbox visualization image storage dir path
    """    

    with open(csv_path, 'r') as f:
        rdr = csv.reader(f)
        cnt = 0
        code_str = ""

        img = cv2.imread(source)

        # json 형태의 csv 파일을 줄 단위로 읽어와 str로 저장
        for line in rdr:
            if len(line) > 1:
                code_str += line[0].replace(" ", "") + "," + line[1].replace(" ", "")
            else:
                code_str += line[0].replace(" ", "")

            cnt = cnt + 1 if line[0].replace(" ", "") == "}" else 0
            if cnt > 3: break

    code_str += "}"

    # eval func을 통해 str -> dict 변환
    annotation = eval(code_str)['images'][source.split("/")[-1]]["words"]

    for i in annotation:
        A = annotation[i]['points']
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


def viz_json_exp()->None:
    json_path = '/data/ephemeral/home/data/medical/ufo/train.json'
    source = '/data/ephemeral/home/data/medical/img/train/drp.en_ko.in_house.deepnatural_002754.jpg'
    output_dir = '/data/ephemeral/home/save_bbox' 
    visualize_annotations_json(json_path, source, output_dir)

def viz_csv_exp()->None:
    csv_path='/data/ephemeral/home/output.csv'
    source = '/data/ephemeral/home/data/medical/img/test/drp.en_ko.in_house.deepnatural_003400.jpg'
    output_dir = '/data/ephemeral/home/save_bbox' 
    visualize_annotations_csv(csv_path, source, output_dir)
