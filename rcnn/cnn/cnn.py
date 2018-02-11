from keras.models import load_model


class CNN:

    def __init__(self):
        self.model = load_model('/home/devfoo/Dev/Studium/ISY/keras_model.h5')

    def predIfIsBeer(self, x):
        Y = self.model.predict(x, batch_size=32)
        Y_return = []
        for y in Y:  # i think there must be a numpy method to do this, but this works for now
            p_beer = y[1]
            if p_beer > 0.8:
                Y_return.append(1)
            else:
                Y_return.append(0)
        return Y_return