# http://cs.brown.edu/~pff/papers/seg-ijcv.pdf

import os
import uuid

import cv2
import numpy as np

from rcnn.selectivesearch.selectivesearch import selectivesearch
from rcnn.utils.dataset import Dataset

dataset = Dataset('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/SPLIT/split8020/test')
path_nobeer = '/home/devfoo/Dev/Studium/ISY/data/nobeer/test'
path_beer = '/home/devfoo/Dev/Studium/ISY/data/beer/test'
square_size = 50
ss_scale = 500
ss_sigma = 0.8
ss_min_size = 100

def store_beer_sample(img):
    _store_sample(path_beer, img)

def store_nobeer_sample(img):
    _store_sample(path_nobeer, img)

def _store_sample(path, img):
    id = uuid.uuid4()
    cv2.imwrite(path + os.sep + str(id) + '.jpg', img)

for n in dataset.fileIds:
    img = dataset.getPicture(n)
    img_no_beer = img.copy()
    # get beer bottle and store training sample in 4 different rotation angles
    for bb in dataset.getDescription(n):
        print(n)
        img_beer_cropped = img[bb['y']:bb['y'] + bb['h'],bb['x']:bb['x'] + bb['w']]
        img_beer_cropped_resized = cv2.resize(img_beer_cropped,(square_size, square_size))
        for i in range(0,4):
            store_beer_sample(np.rot90(img_beer_cropped_resized, i))

        # remove beer from no-beer image
        cv2.rectangle(img_no_beer, (bb['x'], bb['y']), (bb['x'] + bb['w'], bb['y'] + bb['h']), (0,0,0), thickness=-1)

    img_lbl, regions = selectivesearch.selective_search(img_no_beer, scale=ss_scale, sigma=ss_sigma, min_size=ss_min_size)
    for region in regions:
        x0, y0, w, h = region['rect']
        if w == 0 or h == 0:
            continue
        x1 = x0 + w
        y1 = y0 + h
        sample_region_no_beer = img_no_beer[y0:y1,x0:x1]
        sample_region_no_beer_resized = cv2.resize(sample_region_no_beer, (square_size, square_size))
        store_nobeer_sample(sample_region_no_beer_resized)