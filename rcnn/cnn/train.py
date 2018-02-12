from glob import glob

import cv2
import numpy as np
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Dropout
from keras.models import Sequential
# https://chsasank.github.io/keras-tutorial.html
from keras.utils import np_utils

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(50, 50, 3)))
model.add(Conv2D(filters=32, kernel_size=1, activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Conv2D(filters=64, kernel_size=1, activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(units=512, activation='relu'))
model.add(Dense(units=2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

x = []
y = []
x_eval = []
y_eval = []
for filename in glob('/home/devfoo/Dev/Studium/ISY/data/beer/train/*.jpg'):
    y.append(1)
    img = cv2.imread(filename)
    x.append(img)

for filename in glob('/home/devfoo/Dev/Studium/ISY/data/nobeer/train/*.jpg'):
    y.append(0)
    img = cv2.imread(filename)
    x.append(img)

for filename in glob('/home/devfoo/Dev/Studium/ISY/data/beer/test/*.jpg'):
    y_eval.append(1)
    img = cv2.imread(filename)
    x_eval.append(img)

for filename in glob('/home/devfoo/Dev/Studium/ISY/data/nobeer/test_small/*.jpg'):
    y_eval.append(0)
    img = cv2.imread(filename)
    x_eval.append(img)

print('Got',len(x),'training samples and',len(x_eval),'eval samples...')

X_train = np.array(x).astype('float32')
X_eval = np.array(x_eval).astype('float32')
Y_train = np.array(y)
Y_eval = np.array(y_eval)
X_train /= 255
X_eval /= 255
Y_train = np_utils.to_categorical(Y_train, 2)
Y_eval = np_utils.to_categorical(Y_eval, 2)

foo = model.fit(X_train, Y_train, batch_size=32, epochs=10, verbose=1, shuffle=True, validation_data=(X_eval, Y_eval))
model.save('/home/devfoo/Dev/Studium/ISY/keras_model_full-train.h5')