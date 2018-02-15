import cv2

from rcnn.selectivesearchAlpacaDB.selectivesearch import selectivesearch
from rcnn.utils.dataset import Dataset

dataset = Dataset('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL')

# img, n = dataset.getRandomPicture()
img = dataset.getPicture(201)
img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.8, min_size=10)
print('Found',len(regions), 'regions')
for region in regions:
    x0, y0, w, h = region['rect']
    if x0 > 400 and x0 < 600 and w > 50 and h > 50:
        print(x0, y0, w, h)
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (0, 0, 255), thickness=2)

cv2.imwrite('regions_filtered_scale500.jpg', img)
cv2.imshow('image', img)
cv2.waitKey()