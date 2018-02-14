__author__ = 'Robin'

import cv2
import matplotlib.pyplot as plt
import glob
import json

EVAL_IMGS_PATH = './data/beerBottles/eval/'
PRED_PATH = './data/beerBottles/pred/'

def convertToRGB(img):
    '''
        Helper function to convert an image to rgb
    '''
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def detect_objects(cascade, imgPath, colored_img, scaleFactor = 1.1):
    '''
        Detects objects on given image, as trained with given cascade and returns image wirh detected objects
        Also write the found objects into a json file, for evaluation.
    '''
    #just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy()

    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    #let's detect multiscale (some images may be closer to camera than others) images
    objects = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    json_file = open(extract_json_filename(imgPath), mode='w', encoding='utf-8')
    eval_data = []
    #iterate over list of found objects and draw them into the img and write the boxes into the json
    for (x, y, w, h) in objects:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
        eval_data.append({
            'x': int(x),        # must convert it to python int, so the json serializer can put it into json (numpy ints producing errors)
            'y': int(y),
            'w': int(w),
            'h': int(h)
        })
    json.dump(eval_data, json_file)
    json_file.close()
    cv2.imwrite(PRED_PATH + imgPath[-8:], img_copy)
    return img_copy


def extract_json_filename(imgPath):
    '''
    Extract filename of current image and create the json filename from that.
    Returns the json filename
    '''
    filename = imgPath[-8:-3] + 'json'
    print(filename)
    return PRED_PATH + filename


def create_predictions(beer_bottle_filter):
    images = glob.glob(EVAL_IMGS_PATH + '*.jpg')
    #load cascade classifier training file for haarcascade
    #haar_face_cascade = cv2.CascadeClassifier('./data/test/haarcascade_frontalface_alt.xml')
    # TODO Hier den Classifieer Pfad anpassen
    for imgPath in images:
        img = cv2.imread(imgPath)
        detected_img = detect_objects(beer_bottle_filter, imgPath, img, scaleFactor=1.2)
        # TODO auskommentieren wenn keine visuelle Ausgabe gewünscht
        # plt.imshow(convertToRGB(detected_img))
        # plt.show()


def real_time_detection(beer_bottle_filter):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Beer bottle detection')
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        objects = beer_bottle_filter.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in objects:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Beer bottle detection', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


beer_bottle_filter = cv2.CascadeClassifier('./data/beerBottles/cascade/cascade.xml')
#create_predictions(beer_bottle_filter)
real_time_detection(beer_bottle_filter)
