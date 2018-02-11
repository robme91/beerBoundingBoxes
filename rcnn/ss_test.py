import cv2

from rcnn.selectivesearch.selectivesearch import selectivesearch
from rcnn.utils.dataset import Dataset

dataset = Dataset('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL')

img, n = dataset.getRandomPicture()
print(n)
img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.8, min_size=10)
for region in regions:
    x0, y0, w, h = region['rect']
    cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (0, 0, 255), thickness=1)

cv2.imshow('image', img)

cv2.waitKey()
