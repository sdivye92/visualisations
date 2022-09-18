from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import numpy as np

class InvalidArgument(Exception):
    pass

def get_data(method = 'xor'):
    if method == 'xor':
        X = np.array([[0,0],[0,1],[1,0],[1,1]])
        y = np.array([[0],[1],[1],[0]])
        return X, y
    else:
        raise InvalidArgument(f"Invalid data generation method type: {method}")

def plot(X, y, model, step=0.1):
    min1, max1 = X[:,0].min(), X[:,0].max()
    min2, max2 = X[:,1].min(), X[:,1].max()
    x1_scale = np.arange(min1-step, max1+step, step)
    x2_scale = np.arange(min2-step, max2+step, step)
    x_grid, y_grid = np.meshgrid(x1_scale, x2_scale)
    x_g, y_g = x_grid.flatten(), y_grid.flatten()
    x_g, y_g = x_g.reshape((len(x_g), 1)), y_g.reshape((len(y_g), 1))
    grid = np.hstack((x_g, y_g))
    p_pred = model.predict_proba(grid)
    pp_grid = p_pred.reshape(x_grid.shape)
    surface = plt.contourf(x_grid, y_grid, pp_grid)
    plt.colorbar(surface)
    for class_value in range(2):
        row_ix = np.where(y.flatten() == class_value)
        plt.scatter(X[row_ix, 0], X[row_ix, 1], s=100)

X, y = get_data(method = 'xor')
        
model1 = Sequential()
model1.add(Dense(8, input_dim=X.shape[1]))
model1.add(Dense(1))
model1.add(Activation('sigmoid'))
sgd = SGD(lr=0.1)
model1.compile(loss='binary_crossentropy', optimizer=sgd)

model2 = Sequential()
model2.add(Dense(8, input_dim=X.shape[1]))
model2.add(Activation('sigmoid'))
model2.add(Dense(1))
model2.add(Activation('sigmoid'))
sgd = SGD(lr=0.1)
model2.compile(loss='binary_crossentropy', optimizer=sgd)

model3 = Sequential()
model3.add(Dense(8, input_dim=X.shape[1]))
model3.add(Activation('relu'))
model3.add(Dense(1))
model3.add(Activation('sigmoid'))
sgd = SGD(lr=0.1)
model3.compile(loss='binary_crossentropy', optimizer=sgd)

model4 = Sequential()
model4.add(Dense(8, input_dim=X.shape[1]))
model4.add(Activation('tanh'))
model4.add(Dense(1))
model4.add(Activation('sigmoid'))
sgd = SGD(lr=0.1)
model4.compile(loss='binary_crossentropy', optimizer=sgd)

n_epoch = 5000
plt.figure(figsize=(15,10))
for e in range(n_epoch):
    model1.fit(X, y, batch_size=1, epochs=1, verbose=0)
    model2.fit(X, y, batch_size=1, epochs=1, verbose=0)
    model3.fit(X, y, batch_size=1, epochs=1, verbose=0)
    model4.fit(X, y, batch_size=1, epochs=1, verbose=0)
    
    if (e%5 == 0) or (e == (n_epoch-1)):
        plt.clf()
        plt.suptitle(f"Epoch: {e}")
        plt.subplot(221)
        plot(X, y, model1, step=0.1)
        plt.title("Linear activation")
        plt.subplot(222)
        plot(X, y, model2, step=0.1)
        plt.title("Sigmoid activation")
        plt.subplot(223)
        plot(X, y, model3, step=0.1)
        plt.title("Relu activation")
        plt.subplot(224)
        plot(X, y, model4, step=0.1)
        plt.title("Tanh activation")
    plt.pause(0.00001)
        
plt.show()