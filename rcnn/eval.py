import cv2
from rcnn.selectivesearch.selectivesearch import selectivesearch

from rcnn.cnn.cnn import CNN
from rcnn.utils.dataset import Dataset

cnn = CNN()
dataset = Dataset('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/SPLIT/split8020/test')

imgs = []
for imgId in dataset.fileIds:
    img = dataset.getPicture(imgId)
    img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.8, min_size=10)
    beer_regions = []
    for region in regions:
        x0, y0, w, h = region['rect']
        if w == 0 or h == 0:
            continue
        region_img = img[y0:y0 + h, x0:x0 + w]
        region_img = cv2.resize(region_img,(50,50))
        region_img = region_img.reshape(1,50,50,3)
        region_img = region_img.astype('float32')
        region_img /= 255
        if cnn.predIfIsBeer(region_img)[0] == 1:
            beer_regions.append(region)

        # imgs.append(img)
    for b in beer_regions:
        x0, y0, w, h = b['rect']
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), (0, 255, 0), thickness=2)

    if len(beer_regions) != 0:
        cv2.imshow('I think i found stuff!', img)
        cv2.waitKey()


