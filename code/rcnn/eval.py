import json
import random

import cv2
import numpy as np

from rcnn.cnn.cnn import CNN
from rcnn.selectivesearchAlpacaDB.selectivesearch import selectivesearch
from rcnn.utils.dataset import Dataset

square_size = 200
# cnn = CNN('/home/devfoo/Dev/Studium/ISY/keras_model_full-train.h5', 0.5)
# cnn = CNN('/home/devfoo/Dev/Studium/ISY/keras_model_full-train.h5', 0.5)
cnn = CNN('/home/devfoo/Dev/Studium/ISY/bbb_large-1to2.h5', 0.99)
# cnn = CNN('cnn/cnn2.h5', 0.99)
dataset = Dataset('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/SPLIT/split8020/test')
PATH_RESULT_IMG = '/home/devfoo/Dev/Studium/ISY/results/cnn_large_99p/images/'
PATH_RESULT_JSON = '/home/devfoo/Dev/Studium/ISY/results/cnn_large_99p/json/'

imgs = []
fileIds = dataset.fileIds
random.shuffle(fileIds)

for imgId in dataset.fileIds:
    bounding_boxes = []
    print('Testing on image id', imgId)
    img = dataset.getPicture(imgId)
    img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.8, min_size=10)
    beer_region_candidates = []
    print('Selective Search found',len(regions),'regions.')
    for region in regions:
        x0, y0, w, h = region['rect']
        if w == 0 or h == 0:
            region_img = np.zeros((square_size,square_size,3))
            beer_region_candidates.append(region_img)
            continue
        region_img = img[y0:y0 + h, x0:x0 + w]
        region_img = cv2.resize(region_img,(square_size,square_size))
        # region_img = region_img.reshape(1,square_size,square_size,3)
        region_img = region_img.astype('float32')
        region_img /= 255
        beer_region_candidates.append(region_img)

    beer_region_candidates = np.array(beer_region_candidates)
    pred_Y = cnn.predIfIsBeer(beer_region_candidates)
    beer_regions = []
    for y, X in zip(pred_Y, regions): # crappy, can be made faster
        if y == 1:
            print('HIT')
            beer_regions.append(X)

    for b in beer_regions:
        x0, y0, w, h = b['rect']
        bounding_boxes.append({
            'x': x0,
            'y': y0,
            'w': w,
            'h': h
        })
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (0, 255, 0), thickness=2)

    if len(beer_regions) != 0:
        cv2.imwrite(PATH_RESULT_IMG + imgId + '.jpg', img)

    file = open(PATH_RESULT_JSON + imgId + '.json', mode='w', encoding='utf-8')
    json.dump(bounding_boxes, file)
    file.close()

    cv2.imshow('EVAL VIEW', img)
    cv2.waitKey(1)