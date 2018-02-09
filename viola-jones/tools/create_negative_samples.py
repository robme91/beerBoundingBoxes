import glob
import cv2
import json
import numpy as np

#output path for negatives
outputPath = '../data/beerBottles/negatives/negative{}.jpg'
# import positives
images = glob.glob('../data/beerBottles/positives/*.jpg')
# open negative file for training
negativesFile = open('../data/beerBottles/negatives.txt', 'w')

#counter for naming img files
counter = 0
for imgPath in images:
    negative = cv2.imread(imgPath)
    jsonPath = imgPath[0:-3] + 'json'
    bottleJson = json.load(open(jsonPath))
    for beer in bottleJson:
        # put random colored area in img so there is no bottle anymore
        negative[beer['y']:beer['y']+beer['h'], beer['x']:beer['x']+beer['w']] = np.random.randint(256)
    #save negative img
    cv2.imwrite(outputPath.format(counter), negative)
    # write negative img path to file
    negativesFile.write('negatives/negative{}.jpg'.format(counter))
    negativesFile.write('\n')
    counter += 1
    print('Created negative' + str(counter))
