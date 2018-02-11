import json
import os
from random import randint

import cv2


class Dataset:

    def __init__(self, path):
        self.path = path

    def getRandomPicture(self):
        n = randint(0,1000)
        return self.getPicture(n), n

    def getPicture(self, n):
        return cv2.imread(self.path + os.sep + str(n).zfill(4) + '.jpg')

    def getDescription(self, n):
        return json.load(open(self.path + os.sep + str(n).zfill(4) + '.json', mode='r'))

    def getPictureWithoutBeer(self, n):
        orig_image = self.getPicture(n)
        orig_description = self.getDescription(n)
