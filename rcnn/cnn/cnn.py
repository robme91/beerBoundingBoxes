from keras.models import load_model


class CNN:

    def __init__(self, path_to_model, p):
        self.model = load_model(path_to_model)
        self.p = p
    def predIfIsBeer(self, x):
        Y = self.model.predict(x, batch_size=32)
        Y_return = []
        for y in Y:  # i think there must be a numpy method to do this, but this works for now
            p_beer = y[1]
            if p_beer > self.p:
                Y_return.append (1)
            else:
                Y_return.append(0)
        return Y_return