from glob import glob

import cv2
import numpy as np
from keras.layers import Conv2D, Flatten, Dense
from keras.models import Sequential
# https://chsasank.github.io/keras-tutorial.html
from keras.utils import np_utils

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(50, 50, 3)))
# model.add(Conv2D(filters=32, kernel_size=1, activation='relu'))
# model.add(MaxPooling2D((2, 2)))
# model.add(Dropout(0.25))
# model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(filters=64, kernel_size=1, activation='relu'))
# model.add(MaxPooling2D((2, 2)))
# model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(units=512, activation='relu'))
model.add(Dense(units=2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

x_train = []
y_train = []
for filename in glob('/home/devfoo/Dev/Studium/ISY/data/beer/*.jpg'):
    y_train.append(1)
    img = cv2.imread(filename)
    x_train.append(img)

X_train = np.array(x_train).astype('float32')
Y_train = np.array(y_train)
X_train /= 255
y_train = np_utils.to_categorical(y_train, 2)
# X_train = X_train.reshape(X_train.shape[0], 50, 50, 3)

foo = model.fit(X_train, y_train,batch_size=1, epochs=1, verbose=1)