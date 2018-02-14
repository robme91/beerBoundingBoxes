from glob import glob

import cv2
import numpy as np

from rcnn.cnn.cnn import CNN

cnn = CNN('keras_model_less-nobeer.h5')
imgs = []
for filename in glob('/home/devfoo/Dev/Studium/ISY/data/beer/test/*.jpg'):
    img = cv2.imread(filename)
    # img = img.reshape(1,50,50,3)
    img = img.astype('float32')
    img /= 255
    imgs.append(img)

imgs = np.array(imgs)
foo = cnn.predIfIsBeer(imgs)
print(foo)
