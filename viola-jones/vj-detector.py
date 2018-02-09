__author__ = 'Robin'

import cv2
import matplotlib.pyplot as plt
import glob

'''
Helper function to convert an image to rgb
'''
def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

'''
Detects objects on given image, as trained with given cascade and returns image wirh detected objects
'''
def detect_objects(cascade, colored_img, scaleFactor = 1.1):
    #just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy()

    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    #let's detect multiscale (some images may be closer to camera than others) images
    objects = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    #go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in objects:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return img_copy

#test1 = cv2.imread('./test/data/test1.jpg')
images = glob.glob('./data/test/*.jpg')
#load cascade classifier training file for haarcascade
haar_face_cascade = cv2.CascadeClassifier('./data/test/haarcascade_frontalface_alt.xml')
for imgPath in images:
    img = cv2.imread(imgPath)
    detected_img = detect_objects(haar_face_cascade, img, scaleFactor=1.2)
    plt.imshow(convertToRGB(detected_img))
    plt.show()

#convert image to RGB and show image
#detected_img = detect_objects(haar_face_cascade, test1)
#plt.imshow(convertToRGB(detected_img))
#plt.show()